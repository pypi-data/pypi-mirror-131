/*******************************************************************************
 * @file api_impl.cpp
 * @brief api python 接口
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "api_impl.h"

#include <math.h>
#include <algorithm>

#include "time.h"
#include <boost/iostreams/filter/lzma.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <pybind11/embed.h>
#include <pybind11/functional.h>

#include "utils/common.h"
#include "obj.h"
#include "field_mapping.h"
#include "backtest/backtest_report.h"

structlog::Logger logger = structlog::Logger::Root();
std::ofstream g_log_file;
boost::iostreams::filtering_ostream g_log_stream;
using namespace boost::property_tree;

TqPythonApi::TqPythonApi(py::object& account, py::object& auth, py::object& backtest, py::object& gui, py::object& log,
  bool disable_print, const std::string& md_url, int srandom, int64_t mock_date_time)
  : m_account(account)
  , m_last_order_id(0)
  , m_md_url(md_url)
  , m_web_helper(nullptr)
  , m_disable_print(disable_print)
  , m_is_backtest(false)
  , m_sub_instruments(std::make_shared<Subscribed>())
  , random(srandom ? srandom : time(nullptr)) {
  try {
    py::print("在使用天勤量化之前，默认您已经知晓并同意以下免责条款，如果不同意请立即停止使用：" + kDisclaimUrl);

    if (mock_date_time)
      MockDateTime(mock_date_time);

    SetupLogger(log, structlog::LogLevel::Debug);

    SetupAuth(auth);

    SetupBackTest(backtest);

    SetupApi();

    SubscribeInstrumentsInfo();

    Login();

    SetupWebGui(gui);

    SetupTradingStatus();

    TrackOrderStatus();

    AliasFuncWhenSecurities();

  } catch (std::exception& ex) {
    CleanUp();
    throw std::exception(std::logic_error(ex.what()));
  }
}

void TqPythonApi::CleanUp() {
  if (m_auth) {
    m_auth->Logout();
    m_auth = nullptr;
  }

  if (m_api) {
    m_api->CleanUp();
    m_api = nullptr;
  }

  structlog::SetOutput(nullptr);
  boost::iostreams::close(g_log_stream);
  g_log_file.close();
}

bool TqPythonApi::RunOnce(double timeout) {
  if (!m_is_backtest && (std::fabs(timeout - 0) > 0.000001) && (NowAsEpochNano() / 1e9) >= timeout)
    return false;

  auto result = m_api->RunOnce();

  for (auto& [symbol, tick] : m_tick_serial_map) {
    tick->RunOnce();
  }

  for (auto& [_, kline] : m_kline_serial_map) {
    kline->RunOnce();
  }

  for (auto& strategy : m_market_maker_strategys) {
    strategy->RunOnce();
  }

  for (auto& [key, task] : m_target_pos_task_map) {
    if (task->RunOnce() < 0) {
      throw std::logic_error(task->m_status_msg.c_str());
    }
  }

  if (m_trading_status_worker) {
    m_trading_status_worker->RunOnce();
  }

  if (m_is_backtest) {
    if (BackTestServiceStatus::kStopped == m_options.backtest_service->GetStatus()) {
      auto init_balance = m_account.cast<TqSim&>().init_balance;

      BacktestReport cal(m_api, m_disable_print, m_user_key, m_account.cast<TqSim&>().init_balance);
      auto report = cal.GetReport();

      if (m_web_helper) {
        m_web_helper->SetReportResult(report);
        m_web_helper->RunOnce();
        m_web_helper->TearDown();
      }

      CleanUp();
      throw BacktestFinished("回测结束!");
    }

    if (!result && BackTestServiceStatus::kAdvancing == m_options.backtest_service->GetStatus())
      m_options.backtest_service->UpdateDateTime();
  }

  if (m_web_helper)
    m_web_helper->RunOnce();

  return true;
}

TqPythonApi::~TqPythonApi() {
  this->CleanUp();
}

bool TqPythonApi::IsChanging(py::object obj, py::str fields) {
  std::string object_classname = obj.attr("__class__").attr("__name__").cast<std::string>();
  if (object_classname == "DataFrame" || object_classname == "Series") {
    auto key = obj.attr("_key").cast<std::string>();
    if (obj.attr("_df_type").cast<std::string>() == "tick") {
      return m_tick_serial_map[key]->m_tick_series_node->m_snap_version < m_root->m_snap_version ? false : true;
    } else {
      auto field = fields.cast<std::string>();
      return m_kline_serial_map[key]->m_is_kline_changed
        || std::get<0>(m_kline_serial_map[key]->m_latest_fields[field]);
    }
  } else if (object_classname == "Quote") {
    std::string symbol = obj.attr("symbol").cast<std::string>();

    for (auto& [key, node] : m_quotes_view[symbol]->GetCommitNodes()) {
      py::str target_filed("_get_{}"_s.format(fields));
      py::object attr = obj.attr(target_filed);
      // 浮点型数据需要单独进行判断
      std::string type = attr(true).attr("__class__").attr("__name__").cast<std::string>();
      if (type == "float" || type == "double") {
        return !DoubleEqual(attr(true).cast<double>(), attr(false).cast<double>());
      }

      return !attr(true).is(attr(false));
    }

    return false;
  } else if (object_classname == "Order") {
    std::string order_id = obj.attr("order_id").cast<std::string>();
    int unit_id = obj.attr("unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id) + "|" + order_id;

    for (auto& [key, node] : m_orders_views[view_key]->GetCommitNodes()) {
      py::str target_filed("_get_{}"_s.format(fields));
      py::object attr = obj.attr(target_filed);
      // 浮点型数据需要单独进行判断
      std::string type = attr(true).attr("__class__").attr("__name__").cast<std::string>();
      if (type == "float" || type == "double") {
        return !DoubleEqual(attr(true).cast<double>(), attr(false).cast<double>());
      }

      return !attr(true).is(attr(false));
    }

    return false;
  } else if (object_classname == "Position") {
    int unit_id = obj.attr("unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id) + "|" + obj.attr("symbol").cast<std::string>();

    for (auto& [key, node] : m_positions_views[view_key]->GetCommitNodes()) {
      py::str target_filed("_get_{}"_s.format(fields));
      py::object attr = obj.attr(target_filed);
      // 浮点型数据需要单独进行判断
      std::string type = attr(true).attr("__class__").attr("__name__").cast<std::string>();
      if (type == "float" || type == "double") {
        return !DoubleEqual(attr(true).cast<double>(), attr(false).cast<double>());
      }

      return !attr(true).is(attr(false));
    }

    return false;
  }

  return false;
}

bool TqPythonApi::IsChanging(py::object obj, py::list fields_list) {
  for (auto item : fields_list) {
    if (IsChanging(obj, py::str(item))) {
      return true;
    }
  }
  return false;
}

bool TqPythonApi::IsChanging(py::object obj) {
  std::string object_classname = obj.attr("__class__").attr("__name__").cast<std::string>();
  if (object_classname == "DataFrame" || object_classname == "Series") {
    auto key = obj.attr("_key").cast<std::string>();
    auto df_type = obj.attr("_df_type").cast<std::string>();
    if (df_type == "tick") {
      if (!m_tick_serial_map[key]->m_tick_series_node)
        return false;
      return m_tick_serial_map[key]->m_tick_series_node->m_snap_version < m_root->m_snap_version ? false : true;
    } else {
      // Kline 推进一根或者最后一根任一字段发生变化均返回 true
      auto is_changed = m_kline_serial_map[key]->m_is_kline_changed;
      for (auto [field, changed] : m_kline_serial_map[key]->m_latest_fields) {
        is_changed = is_changed || std::get<0>(changed);
      }
      return is_changed;
    }
  } else if (object_classname == "Quote") {
    std::string symbol = obj.attr("symbol").cast<std::string>();
    return m_quotes_view[symbol]->GetCommitNodes().size();
  } else if (object_classname == "Order") {
    int unit_id = obj.attr("unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id) + "|" + obj.attr("order_id").cast<std::string>();
    return m_orders_views[view_key]->GetCommitNodes().size();
  } else if (object_classname == "Orders") {
    int unit_id = obj.attr("_unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id);
    return m_orders_views[view_key]->GetCommitNodes().size();
  } else if (object_classname == "Trades") {
    int unit_id = obj.attr("_unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id);
    return m_trades_views[view_key]->GetCommitNodes().size();
  } else if (object_classname == "Position") {
    int unit_id = obj.attr("unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id) + "|" + obj.attr("symbol").cast<std::string>();
    return m_positions_views[view_key]->GetCommitNodes().size();
  } else if (object_classname == "Positions") {
    int unit_id = obj.attr("_unit_id").cast<int>();
    auto view_key = m_user_key + "|" + std::to_string(unit_id);
    return m_positions_views[view_key]->GetCommitNodes().size();
  } else {
    throw std::exception(std::logic_error("当前数据结构暂不支持 ischanging 用法."));
  }
}

std::shared_ptr<InstrumentNode> TqPythonApi::SubscribeQuote(const std::string& symbol) {
  try {
    // 合约校验.
    auto node = EnsureInsValid(symbol);

    // 订阅合约乘数
    // if (m_quotes_view.find(symbol) != m_quotes_view.end()) {
    //  return node;
    //}

    // 订阅行情
    auto req = std::make_shared<md::SubscribeQuote>();
    req->subscribe_id = std::to_string(random());
    req->symbol_set = m_sub_instruments->SubQuote(symbol).quotes;
    TqSyncRequest(m_api, req);

    // 创建一个视图用于判断该对象的 is_changing .
    m_quotes_view[symbol] = m_db_root->CreateView<Instrument>([=](std::shared_ptr<Instrument> q) {
      return q->symbol == symbol;
    });

    // 等待行情数据就绪
    RunUntilReady(m_api, [&]() {
      auto node = m_db_root->GetNode<Instrument>(symbol);
      return !node->Snap()->exchange_time_str.empty();
    });

    return node;
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<TickWrapper> TqPythonApi::GetTickSerial(const std::string& symbol, int data_length) {
  try {
    EnsureInsValid(symbol);

    if (data_length <= 0) {
      auto msg = "Tick 数据序列长度 " + std::to_string(data_length) + " 错误, 请检查序列长度是否填写正确.";
      throw std::invalid_argument(msg.c_str());
    }

    if (m_tick_serial_map.find(symbol) != m_tick_serial_map.end())
      return m_tick_serial_map[symbol];

    auto tick = std::make_shared<TickWrapper>(data_length);
    m_tick_serial_map[symbol] = tick;

    // 订阅 Tick 数据
    auto req_subscribe_tick = std::make_shared<md::SubscribeChartLatest>();
    req_subscribe_tick->subscribe_id = "tqsdk2_sub_tick_" + TrimSymbol(symbol) + std::to_string((int64_t)this);
    req_subscribe_tick->dur_nano = 0;
    req_subscribe_tick->symbol_list.push_back(symbol);
    req_subscribe_tick->view_width = data_length;
    SyncRequest(m_api, req_subscribe_tick);
    if (req_subscribe_tick->result_code != 0) {
      logger.Info("req_subscribe_tick failed");
      return m_tick_serial_map[symbol];
    }

    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    while (tick->m_last_id == -1) {
      if (std::chrono::steady_clock::now() - start > std::chrono::seconds(60)) {
        auto msg = std::string("获取 ") + symbol + std::string(" 的 Tick 超时, 请检查客户端及网络是否正常.");
        throw std::exception(std::logic_error(msg.c_str()));
      }
      m_api->RunOnce();

      // 回测模式下, 回测状态为 kAdvancing 时, 回测模块才就绪
      if (m_is_backtest && m_options.backtest_service->GetStatus() == md::BackTestServiceStatus::kSubscribed)
        continue;

      auto ticks_root = m_root->GetChild<ApiTreeKey::kMarketData>()->GetChild<md::MdTreeKey::kTicks>();
      tick->m_tick_series_node = ticks_root->GetChild(symbol);
      tick->RunOnce();
    }

    return m_tick_serial_map[symbol];
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<KlineWrapper> TqPythonApi::GetKlineSerial(const std::string& symbol, int duration, int data_length) {
  try {
    EnsureInsValid(symbol);

    if (data_length <= 0)
      throw std::invalid_argument("K 线数据序列长度错误, 请检查参数是否填写正确.");

    if (duration <= 0 || (duration > 86400 && duration % 86400 != 0)) {
      throw std::invalid_argument("K 线数据周期 " + std::to_string(duration) + " 错误, 请检查参数是否填写正确.");
    }

    auto kline_key = symbol + std::to_string(duration);
    if (m_kline_serial_map.find(kline_key) != m_kline_serial_map.end())
      return m_kline_serial_map[kline_key];

    m_kline_serial_map[kline_key] = std::make_shared<KlineWrapper>(duration, data_length);

    auto req_subscribe_kline = std::make_shared<md::SubscribeChartLatest>();
    req_subscribe_kline->subscribe_id = "tqsdk2_sub_kline_" + TrimSymbol(kline_key) + std::to_string((int64_t)this);
    req_subscribe_kline->dur_nano = duration * 1000000000LL;
    req_subscribe_kline->symbol_list.push_back(symbol);
    req_subscribe_kline->view_width = data_length;
    SyncRequest(m_api, req_subscribe_kline);
    if (req_subscribe_kline->result_code != 0) {
      logger.Info("req_subscribe_kline failed");
      return m_kline_serial_map[kline_key];
    }

    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    while (m_kline_serial_map[kline_key]->m_last_id == -1) {
      if (std::chrono::steady_clock::now() - start > std::chrono::seconds(60)) {
        auto msg = "获取 " + symbol + " (" + std::to_string(duration) + ") 的K线超时，请检查客户端及网络是否正常.";
        throw std::exception(std::logic_error(msg.c_str()));
      }

      m_api->RunOnce();
      // 1 - 回测模式下, 回测状态为 kAdvancing 时, 回测模块才就绪
      if (m_is_backtest && m_options.backtest_service->GetStatus() == md::BackTestServiceStatus::kSubscribed)
        continue;

      auto node = m_root->GetChild<ApiTreeKey::kMarketData>()->GetChild<md::MdTreeKey::kKlines>()->GetChild(symbol);
      if (node)
        m_kline_serial_map[kline_key]->m_kline_series_node = node->GetChild(req_subscribe_kline->dur_nano);

      m_kline_serial_map[kline_key]->RunOnce();
    }

    return m_kline_serial_map[kline_key];
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<future::OrderNode> TqPythonApi::InsertOrder(const std::string& symbol, const std::string& direction,
  const std::string& offset, int volume, py::object& limit_price, int unit_id) {
  try {
    // 确保合约正确， 同时订阅合约的行情.
    auto node = EnsureInsValid(symbol);
    if (node->Snap()->exchange_time_str.empty())
      SubscribeQuote(symbol);

    if (volume <= 0)
      throw std::invalid_argument("下单数量 " + std::to_string(volume) + " 错误, 请检查 volume 是否填写正确.");

    m_auth->HasTdGrant(symbol, node->Latest()->product_class);

    auto req = std::make_shared<future::InsertOrder>(m_user_key);
    req->unit_id = GetCurrentUnitID(unit_id);
    req->direction = GetDirection(direction);
    req->offset = GetOffSet(offset);
    req->exchange_id = symbol.substr(0, symbol.find("."));
    req->instrument_id = symbol.substr(symbol.find(".") + 1);
    if (limit_price.is_none()) {  //价格为空, 市价单.
      if (AnyOne(req->exchange_id, "CFFEX", "SHFE", "INE", "SSE", "SZSE")) {
        throw std::invalid_argument(symbol + " 不支持市价单, 请使用 limit_price 参数指定价格.");
      }
      req->price_type = future::PriceType::kAny;
      req->time_condition = future::OrderTimeCondition::kIoc;
    } else {
      double price = limit_price.cast<double>();
      if (std::isnan(price)) {
        throw std::invalid_argument("合约价格非法, 请检查价格是否填写正确.");
      }
      req->limit_price = price;
      req->price_type = future::PriceType::kLimit;
      req->time_condition = future::OrderTimeCondition::kGfd;
    }
    req->volume = volume;
    req->volume_condition = future::OrderVolumeCondition::kAny;

    TqSyncRequest(m_api, req);

    // 创建该笔订单的 view 供 ischanging 判断使用
    auto view_key = m_user_key + "|" + std::to_string(req->unit_id) + "|" + req->order_id;
    m_orders_views[view_key] = m_db_root->CreateView<Order>([=](std::shared_ptr<Order> o) {
      return o->order_id == req->order_id;
    });

    auto insert_order_node = m_db_root->GetNode<Order>(m_user_key + "|" + req->order_id);
    if (req->result_code != 0 && insert_order_node == nullptr) {
      auto o = std::make_shared<Order>();
      o->order_id = "tqsdk2|" + std::to_string((int64_t)this) + "|" + std::to_string(++m_last_order_id);
      o->exchange_id = req->exchange_id;
      o->instrument_id = req->instrument_id;
      o->direction = req->direction;
      o->price_type = req->price_type;
      o->limit_price = req->limit_price;
      o->offset = req->offset;
      o->time_condition = req->time_condition;
      o->volume_condition = req->volume_condition;
      o->volume_orign = req->volume;
      o->volume_left = req->volume;
      o->status = OrderStatus::kDead;
      o->status_msg = req->result_msg;
      o->user_key = m_user_key;
      Notify("通知: 下单失败, 委托单ID:" + o->order_id + ", " + req->result_msg);
      return m_db_root->ReplaceRecord<Order>(o);
    }

    return insert_order_node;
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<security::OrderNode> TqPythonApi::InsertStockOrder(
  const std::string& symbol, const std::string& direction, int volume, py::object& limit_price) {
  try {
    if (volume <= 0) {
      throw std::invalid_argument("下单股数 " + std::to_string(volume) + " 错误, 请检查 volume 是否填写正确.");
    }

    auto node = EnsureInsValid(symbol);
    if (node->Snap()->exchange_time_str.empty()) {
      SubscribeQuote(symbol);
    }

    m_auth->HasTdGrant(symbol, node->Latest()->product_class);

    auto req = std::make_shared<security::InsertOrder>(m_user_key);
    req->exchange_id = symbol.substr(0, symbol.find("."));
    req->instrument_id = symbol.substr(symbol.find(".") + 1);
    req->direction = direction == "BUY" ? security::Direction::kBuy : security::Direction::kSell;
    if (limit_price.is_none()) {
      req->price_type = security::PriceType::kAny;
    } else {
      double price = limit_price.cast<double>();
      if (std::isnan(price)) {
        throw std::invalid_argument("委托价格非法, 请检查价格是否填写正确.");
      }
      req->limit_price = price;
      req->price_type = security::PriceType::kLimit;
    }
    req->volume = volume;
    TqSyncRequest(m_api, req);

    // 创建该笔订单的 view 供 ischanging 判断使用
    auto view_key = m_user_key + "|" + req->order_id;
    m_securities_orders_views[view_key] =
      m_db_root->CreateView<security::Order>([=](std::shared_ptr<security::Order> o) {
        return o->order_id == req->order_id;
      });

    auto insert_order_node = m_db_root->GetNode<security::Order>(view_key);
    if (req->result_code != 0 && insert_order_node == nullptr) {
      auto o = std::make_shared<security::Order>();
      o->order_id = "tqsdk2|" + std::to_string((int64_t)this) + "|" + std::to_string(++m_last_order_id);
      o->exchange_id = req->exchange_id;
      o->instrument_id = req->instrument_id;
      o->direction = req->direction;
      o->price_type = req->price_type;
      o->limit_price = req->limit_price;
      o->volume_orign = req->volume;
      o->volume_left = req->volume;
      o->status = security::OrderStatus::kDead;
      o->status_msg = req->result_msg;
      o->user_key = m_user_key;
      Notify("通知: 下单失败, 委托单ID:" + o->order_id + ", " + req->result_msg);
      return m_db_root->ReplaceRecord<security::Order>(o);
    }

    return insert_order_node;
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

void TqPythonApi::CancelOrder(py::object& o) {
  if (o.is_none())
    throw std::invalid_argument("撤单失败, 委托或委托单号不能为空.");

  std::string name = o.attr("__class__").attr("__name__").cast<std::string>();
  auto order_id = name == "Order" ? o.attr("order_id").cast<std::string>() : o.cast<std::string>();

  auto req = std::make_shared<future::CancelOrder>(m_user_key);
  req->order_id = order_id;
  m_api->AsyncRequest(req, [=](std::shared_ptr<UserCommand> rsp) {
    if (rsp->status == UserCommand::Status::kFinished) {
      Notify("通知: 委托单ID:" + order_id + ", " + rsp->result_msg);
    }
  });
}

void TqPythonApi::CancelStockOrder(py::object& o) {
  if (o.is_none())
    throw std::invalid_argument("撤单失败, 委托或委托单号不能为空.");

  std::string name = o.attr("__class__").attr("__name__").cast<std::string>();
  auto order_id = name == "SecuritiesOrder" ? o.attr("order_id").cast<std::string>() : o.cast<std::string>();

  auto req = std::make_shared<security::CancelOrder>(m_user_key);
  req->order_id = order_id;
  m_api->AsyncRequest(req, [=](std::shared_ptr<UserCommand> rsp) {
    if (rsp->status == UserCommand::Status::kFinished) {
      Notify("通知: 委托单ID:" + order_id + ", " + rsp->result_msg);
    }
  });
}

std::shared_ptr<future::OrderNode> TqPythonApi::GetOrder(const std::string& order_id, int unit_id) {
  return m_db_root->GetNode<Order>(m_user_key + "|" + order_id);
}

std::shared_ptr<security::OrderNode> TqPythonApi::GetStockOrder(const std::string& order_id) {
  auto key = m_user_key + "|" + order_id;
  return m_db_root->GetNode<security::Order>(key);
}

const std::map<std::string, std::shared_ptr<OrderNode>>& TqPythonApi::GetOrders(int unit_id) {
  try {
    auto id = GetCurrentUnitID(unit_id);
    auto view_key = m_user_key + "|" + std::to_string(id);

    if (m_orders_views.find(view_key) != m_orders_views.end()) {
      return m_orders_views[view_key]->GetNodes();
    }

    m_orders_views[view_key] = m_db_root->CreateView<Order>(
      [=](std::shared_ptr<Order> o) {
        return o->user_key == m_user_key && (id == ktrade_unit_unset ? 1 : id == o->unit_id);
      },
      [&](std::shared_ptr<Order> o) {
        return o->order_id;
      });

    return m_orders_views[view_key]->GetNodes();
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

const std::map<std::string, std::shared_ptr<security::OrderNode>>& TqPythonApi::GetStockOrders() {
  try {
    // view key
    auto key = m_user_key;

    if (m_securities_orders_views.find(key) == m_securities_orders_views.end()) {
      m_securities_orders_views[key] = m_db_root->CreateView<security::Order>(
        [=](std::shared_ptr<security::Order> o) {
          return o->user_key == m_user_key;
        },
        [&](std::shared_ptr<security::Order> o) {
          return o->order_id;
        });
    }

    return m_securities_orders_views[key]->GetNodes();
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<future::TradeNode> TqPythonApi::GetTrade(const std::string& trade_id, int unit_id) {
  return m_db_root->GetNode<Trade>(m_user_key + "|" + trade_id);
}

std::shared_ptr<security::TradeNode> TqPythonApi::GetStockTrade(const std::string& trade_id) {
  return m_db_root->GetNode<security::Trade>(m_user_key);
}

const std::map<std::string, std::shared_ptr<TradeNode>>& TqPythonApi::GetTrades(int unit_id) {
  try {
    auto trading_unit = GetCurrentUnitID(unit_id);

    auto view_key = m_user_key + "|" + std::to_string(trading_unit);

    if (m_trades_views.find(view_key) != m_trades_views.end()) {
      return m_trades_views[view_key]->GetNodes();
    }

    m_trades_views[view_key] = m_db_root->CreateView<Trade>(
      [=](std::shared_ptr<Trade> t) {
        return t->user_key == m_user_key && (trading_unit == ktrade_unit_unset ? 1 : t->unit_id == trading_unit);
      },
      [&](std::shared_ptr<Trade> t) {
        return t->exchange_trade_id + "|" + t->exchange_order_id;
      });

    return m_trades_views[view_key]->GetNodes();
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

const std::map<std::string, std::shared_ptr<security::TradeNode>>& TqPythonApi::GetStockTrades() {
  try {
    if (m_stock_trades_views.find(m_user_key) == m_stock_trades_views.end()) {
      m_stock_trades_views[m_user_key] = m_db_root->CreateView<security::Trade>(
        [=](std::shared_ptr<security::Trade> t) {
          return t->user_key == m_user_key;
        },
        [&](std::shared_ptr<security::Trade> t) {
          return t->exchange_trade_id;
        });
    }

    return m_stock_trades_views[m_user_key]->GetNodes();
  } catch (std::exception e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

std::shared_ptr<Position> TqPythonApi::GeneratePosition(const std::string& symbol, int unit_id) {
  auto p = std::make_shared<Position>();
  p->user_key = m_user_key;
  p->unit_id = unit_id;
  p->investor_id = m_user_key;
  p->exchange_id = symbol.substr(0, symbol.find("."));
  p->instrument_id = symbol.substr(symbol.find(".") + 1);
  p->ins_pointer.key = symbol;
  p->ins_pointer.node = m_db_root->GetNode<Instrument>(symbol);
  return p;
}

std::shared_ptr<future::PositionNode> TqPythonApi::GetPosition(const std::string& symbol, int unit_id) {
  auto trading_unit = GetCurrentUnitID(unit_id);

  std::string position_key = m_user_key + "|" + std::to_string(trading_unit) + "|" + symbol;
  m_positions_views[position_key] = m_db_root->CreateView<Position>([=](std::shared_ptr<Position> content) {
    return content->unit_id == trading_unit && content->user_key == m_user_key && content->symbol() == symbol;
  });

  auto position_node = m_positions_views[position_key]->GetNodes();
  if (position_node.empty()) {
    return m_db_root->ReplaceRecord(GeneratePosition(symbol, trading_unit));
  }

  return position_node.at(position_key);
}

std::shared_ptr<security::PositionNode> TqPythonApi::GetStockPosition(const std::string& symbol) {
  std::string key = m_user_key + "|" + symbol;

  if (m_securities_positions_views.find(key) != m_securities_positions_views.end()) {
    return m_securities_positions_views[key]->GetNodes().at(key);
  }

  m_securities_positions_views[key] =
    m_db_root->CreateView<security::Position>([=](std::shared_ptr<security::Position> p) {
      return p->user_key == m_user_key && p->symbol() == symbol;
    });

  auto node = m_securities_positions_views[key]->GetNodes();
  if (node.empty()) {
    auto p = std::make_shared<security::Position>();
    p->user_key = m_user_key;
    p->investor_id = m_user_key;
    p->exchange_id = symbol.substr(0, symbol.find("."));
    p->instrument_id = symbol.substr(symbol.find(".") + 1);
    p->ins_pointer.key = symbol;
    p->ins_pointer.node = m_db_root->GetNode<Instrument>(symbol);
    return m_db_root->ReplaceRecord(p);
  }

  return node.at(key);
}

const std::map<std::string, std::shared_ptr<PositionNode>>& TqPythonApi::GetPositions(int unit_id) {
  auto trading_unit = GetCurrentUnitID(unit_id);
  auto view_key = m_user_key + "|" + std::to_string(trading_unit);

  if (m_positions_views.find(view_key) != m_positions_views.end()) {
    return m_positions_views[view_key]->GetNodes();
  }

  if (trading_unit != ktrade_unit_unset) {
    m_positions_views[view_key] = m_api->GetTradeUnitService()->GetTradingUnitNodeDb()->CreateView<Position>(
      [=](std::shared_ptr<Position> content) {
        return content->unit_id == trading_unit && content->user_key == m_user_key;
      },
      [&](std::shared_ptr<Position> content) {
        return content->symbol();
      });
  } else {
    m_positions_views[view_key] = m_db_root->CreateView<Position>(
      [=](std::shared_ptr<Position> content) {
        return content->user_key == m_user_key;
      },
      [&](std::shared_ptr<Position> content) {
        return content->symbol();
      });
  }

  return m_positions_views[view_key]->GetNodes();
}

const std::map<std::string, std::shared_ptr<security::PositionNode>>& TqPythonApi::GetStockPositions() {
  if (m_securities_positions_views.find(m_user_key) != m_securities_positions_views.end()) {
    return m_securities_positions_views[m_user_key]->GetNodes();
  }

  m_securities_positions_views[m_user_key] = m_db_root->CreateView<security::Position>(
    [=](std::shared_ptr<security::Position> content) {
      return content->user_key == m_user_key;
    },
    [&](std::shared_ptr<security::Position> content) {
      return content->symbol();
    });

  return m_securities_positions_views[m_user_key]->GetNodes();
}

std::shared_ptr<future::AccountNode> TqPythonApi::GetAccount(int unit_id) {
  try {
    auto trading_unit = GetCurrentUnitID(unit_id);
    std::string account_key = m_user_key + "|" + std::to_string(trading_unit) + "|CNY";

    auto account4 = m_db_root->GetNodeMap<security::Account>();

    if (trading_unit == ktrade_unit_unset) {
      return m_db_root->GetNode<Account>(account_key);
    }

    return m_api->GetTradeUnitService()->GetTradingUnitNodeDb()->GetNode<Account>(account_key);
  } catch (std::exception& ex) {
    CleanUp();
    throw std::exception(std::logic_error(ex.what()));
  }
}

std::shared_ptr<security::AccountNode> TqPythonApi::GetStockAccount() {
  try {
    std::string account_key = m_user_key + "|CNY";
    return m_db_root->GetNode<security::Account>(account_key);
  } catch (std::exception& ex) {
    CleanUp();
    throw std::exception(std::logic_error(ex.what()));
  }
}

void TqPythonApi::SetupAuth(const py::object& auth) {
  if (py::isinstance<TqAuth>(auth)) {
    m_auth = std::make_shared<TqAuth>(auth.cast<TqAuth&>());
  } else if (py::isinstance<py::str>(auth)) {
    auto user = py::str(auth).cast<std::string>();
    m_auth = std::make_shared<TqAuth>(user.substr(0, user.find(",")), user.substr(user.find(",") + 1));
  } else {
    throw std::invalid_argument("用户权限认证失败, 请输入正确的信易账户信息.");
  }
}

void TqPythonApi::SetupLogger(const py::object& log, structlog::LogLevel level) {
  structlog::SetLevel(level);

  auto conf = py::str(log).cast<std::string>();
  if (conf.compare("False") != 0) {
#ifdef _WIN32
    fs::path log_path = fs::current_path() / "tqsdk2" / "logs";
#else
    fs::path log_path = "/tmp/tqsdk2/logs";
#endif
    fs::create_directories(log_path);
    fs::path log_file = log_path / conf;
    if (!conf.compare("True")) {
      log_file = log_path / (NowAsString() + "-" + std::to_string(GetPID()) + ".log");
    }
    g_log_file = std::ofstream(log_file.string(), std::ios_base::out | std::ios::binary);
    g_log_stream.push(g_log_file);
  }
  structlog::SetOutput(&g_log_stream);
}

void TqPythonApi::SetupBackTest(const py::object& backtest) {
  if (!py::isinstance<BackTest>(backtest))
    return;

  // if (!m_auth->HasGrant(kAuthBackTest))
  //  throw std::invalid_argument("您的账户暂不支持回测功能，需要升级专业版本后使用。升级网址：" + kAccountUrl);

  if (!py::isinstance<TqSim>(m_account))
    throw std::invalid_argument("回测时, 账户类型必须为TqSim.");

  m_is_backtest = true;
  m_options.backtest_service = backtest.cast<BackTest&>().GetService();
}

void TqPythonApi::SetupApi() {
  auto& account = m_account.cast<TqUser&>();

  m_options.trade_unit_path = account.m_trading_unit->GetTradeUnitPath();
  m_options.md_url = m_md_url;
  m_options.enable_sync_position_volume = true;
  m_options.access_token = m_auth->GetAccessToken();
  m_options.his_record_mode = true;
  m_api = TqApi::Create(m_options, &logger);
}

void TqPythonApi::SubscribeInstrumentsInfo() {
  if (m_is_backtest)
    return;

  auto req = std::make_shared<md::SubscribeObjectInfo>();
  req->subscribe_id = std::to_string(random());
  req->time_out_interval = 30000;
  req->product_class_filter = {md::ProductClass::kFuture, md::ProductClass::kStock};
  req->expired_type = ExpiredType::kBoth;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    throw std::exception(std::logic_error("订阅合约信息失败."));
  }
  logger.Info("合约信息订阅完成.");
}

void TqPythonApi::Login() {
  auto& account = m_account.cast<TqUser&>();

  Notify("通知: 与交易服务器的网络连接已建立.");
  auto notice_view = m_api->DataDb()->CreateView<Notice>();
  notice_view->AfterCommit(std::to_string((int64_t)this), [=](std::shared_ptr<NoticeNode> node) -> void {
    Notify("通知: " + node->Latest()->content);
  });

  account.SetAuth(m_auth).Login(m_api).PostLogin(m_api);

  m_user_key = account.m_user_key;
  m_root = m_api->DataRoot();
  m_db_root = m_api->DataDb();
  if (account.m_trading_unit->IsEnable()) {
    m_trade_unit_root = m_api->GetTradeUnitService()->GetTradingUnitNodeDb();
  }

  // 确认行情服务器连接完成
  RunUntilReady(m_api, [&]() -> bool {
    auto login = m_db_root->GetNode<md::Session>("md_session");
    if (login == nullptr) {
      return false;
    }

    if (m_is_backtest && !login->Snap()->error_msg.compare(0, 26, "Backtest Permission Denied")) {
      throw std::exception(std::logic_error(
        "免费账户每日可以回测3次，今日暂无回测权限，需要购买专业版本后使用。升级网址：" + kAccountUrl));
    }

    return login->Snap()->session_status == md::SessionStatus::kLogined;
  });
  Notify("通知: 与合约服务器的网络连接已建立.");
}

void TqPythonApi::TrackOrderStatus() {
  m_alive_order_view = m_db_root->CreateView<TqApiViewKey, Order>(TqApiViewKey::kAliveOrder);
  m_alive_order_view->AfterCommit(std::to_string((int64_t)this), [&](std::shared_ptr<OrderNode> node) -> void {
    std::string msg = "通知: ";
    msg += "订单号:" + node->Snap()->order_id + ", 开平:" + GetOffSet(node->Snap()->offset) + ", 方向:"
      + GetDirection(node->Snap()->direction) + std::string(", 委托数量:") + std::to_string(node->Snap()->volume_orign)
      + std::string(", 未成交数量:") + std::to_string(node->Snap()->volume_left) + std::string(", 价格:")
      + std::to_string(node->Snap()->limit_price) + std::string(", 状态:") + GetStatus(node);
    if (!node->Snap()->status_msg.empty()) {
      msg += std::string(", 信息:") + node->Latest()->status_msg;
    }
    Notify(msg);
  });
}

void TqPythonApi::AliasFuncWhenSecurities() {
  auto& account = m_account.cast<TqUser&>();
  if (account.m_type == AccountType::kSecurities) {
    py::exec(R"(
        TqApi.get_account = TqApi._get_stock_account
        TqApi.get_order = TqApi._get_stock_order
        TqApi.get_trade = TqApi._get_stock_trade
        TqApi.get_position = TqApi._get_stock_position
        TqApi.insert_order = TqApi._insert_stock_order
        TqApi.cancel_order = TqApi._cancel_stock_order
    )");
  }
}

void TqPythonApi::Notify(const std::string& msg) {
  if (m_disable_print)
    return;

  // 回测模式下, 通知时间为回测的时间
  auto current_dt = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : NowAsEpochNano();

  py::gil_scoped_acquire acquire;
  py::print(EpochNanoToHumanTime(current_dt), "-", msg);
  py::gil_scoped_release release;
}

void TqPythonApi::SetupWebGui(const py::object& web_gui) {
  auto web_conf = py::str(web_gui).cast<std::string>();
  if (!web_conf.compare("False"))
    return;

  auto& u = m_account.cast<TqUser&>();
  m_web_helper = std::make_shared<CWebHelper>(m_api, u.m_login_req->bid, u.m_login_req->user_id, m_user_key);
  m_web_helper->SetBacktest(m_options.backtest_service).SetSubscribles(m_sub_instruments).Run(web_conf);
}

void TqPythonApi::SetupTradingStatus() {
  m_trading_status_worker = std::make_shared<TradingStatusWorker>(m_api, logger, m_auth->GetAccessToken());
}

int TqPythonApi::GetCurrentUnitID(int unit_id) {
  auto& account = m_account.cast<TqUser&>();

  if (unit_id != ktrade_unit_unset && (unit_id < 1 || unit_id > 99))
    throw std::invalid_argument("交易单元指定错误, 交易单元仅支持 1 - 99 中的数字类型.");

  if (account.m_trading_unit->IsEnable() && !m_auth->HasGrant(kAuthTradingUnit))
    throw std::invalid_argument("您的账户暂不支持交易单元功能, 需要购买专业版本后继续使用。升级网址：" + kAccountUrl);

  if (unit_id != ktrade_unit_unset && account.m_login_req->backend == BackEnd::kLocalSim)
    throw std::invalid_argument("本地模拟账户 TqSim 暂不支持交易单元功能.");

  if (!account.m_trading_unit->IsEnable() && unit_id != ktrade_unit_unset)
    throw std::invalid_argument("交易单元功能未启用, 请在初始化账户实例时指定默认交易单元.");

  return unit_id == ktrade_unit_unset ? account.m_trading_unit->GetDefaultUnitID() : unit_id;
}

std::vector<int> TqPythonApi::GetTradingUnits() {
  std::vector<int> units;
  auto positions_view = m_trade_unit_root->CreateView<Position>([&](std::shared_ptr<Position> p) {
    return p->user_key == m_user_key;
  });

  for (auto [key, node] : positions_view->GetNodes()) {
    if (std::find(units.begin(), units.end(), node->Snap()->unit_id) != units.end())
      continue;
    units.push_back(node->Snap()->unit_id);
  }

  return units;
}

void TqPythonApi::DeleteTradingUnits(py::object unit_id) {
  try {
    auto& account = m_account.cast<TqUser&>();
    if (account.m_trading_unit->IsEnable() && !m_auth->HasGrant(kAuthTradingUnit))
      throw std::invalid_argument("您的账户暂不支持交易单元功能, 需要购买专业版本后使用。升级网址：" + kAccountUrl);

    if (py::isinstance<py::str>(unit_id) && unit_id.cast<std::string>() == "ALL") {
      m_api->GetTradeUnitService()->DeleteTradingUnit(m_user_key);
      return;
    }

    auto delete_unit_id = unit_id.cast<int>();
    if (delete_unit_id != ktrade_unit_unset && (delete_unit_id < 1 || delete_unit_id > 99))
      throw std::invalid_argument("交易单元指定错误, 交易单元仅支持 1 - 99 中的数字类型.");

    m_api->GetTradeUnitService()->DeleteTradingUnit(m_user_key, delete_unit_id);
  } catch (std::exception& e) {
    CleanUp();
    throw std::exception(std::logic_error(e.what()));
  }
}

void TqPythonApi::AddMarketMakerStrategy(std::shared_ptr<extension::MarketMakerStrategy> mm) {
  if (!m_auth->HasGrant(kAuthMarketMaker)) {
    std::string msg = "您的账户不支持做市模块，需要购买专业版本后使用。升级网址：https://account.shinnytech.com";
    throw std::invalid_argument(msg.c_str());
  }

  if (std::find(m_market_maker_strategys.begin(), m_market_maker_strategys.end(), mm) != m_market_maker_strategys.end())
    return;

  m_market_maker_strategys.push_back(mm);
}

py::object TqPythonApi::GetDataFrame(const std::string& df_type, const std::string& key, int row, int column,
  std::vector<double>& data, const py::list& column_list, py::object& obj) {
  py::object pandas = py::module::import("pandas");
  py::object df = pandas.attr("DataFrame")(
    py::array_t<double>({row, column}, {column * sizeof(double), sizeof(double)}, data.data(), obj), "copy"_a = false,
    "columns"_a = column_list);

  py::object origin_constructor = df.attr("_constructor_sliced");
  df.attr("_constructor_sliced") = py::cpp_function([=](py::args args, py::kwargs kwargs) {
    auto series = origin_constructor(*args, **kwargs);
    series.attr("_key") = key;
    series.attr("_df_type") = df_type;
    return series;
  });
  df.attr("_key") = key;
  df.attr("_df_type") = df_type;

  return df;
}

inline std::shared_ptr<ContentNode<Instrument>> TqPythonApi::EnsureInsValid(const std::string& symbol) {
  auto exchange_id = symbol.substr(0, symbol.find("."));
  if (AnyOne(exchange_id, "SHFE", "DCE", "CZCE", "INE", "CFFEX", "KQ", "SSWE") && !m_auth->HasGrant("futr")) {
    throw std::exception(
      std::logic_error("您的账户不支持期货行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  if (AnyOne(exchange_id, "SSE", "SZSE") && !m_auth->HasGrant("sec")) {
    throw std::exception(
      std::logic_error("您的账户不支持股票行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  if (AnyOne(symbol, "SSE.000016", "SSE.000300", "SSE.000905") && !m_auth->HasGrant("lmt_idx")) {
    throw std::exception(
      std::logic_error("您的账户不支持指数行情，需升级后使用。升级网址：https://account.shinnytech.com."));
  }

  auto symbol_node = m_db_root->GetNode<Instrument>(symbol);
  if (!symbol_node && !SubscribleInstrumens(symbol)) {
    throw std::invalid_argument("合约代码 " + symbol + " 不存在, 请检查合约代码是否填写正确.");
  }

  if (!m_db_root->GetNode<Instrument>(symbol)) {
    throw std::invalid_argument("合约代码 " + symbol + " 不存在, 请检查合约代码是否填写正确.");
  }

  return m_db_root->GetNode<Instrument>(symbol);
}

std::vector<std::string> TqPythonApi::QueryQuotes(const std::string& ins_class, const std::string& exchange_id,
  const std::string& product_id, py::object& expired, py::object& has_night) {
  std::vector<ProductClass> product_class;
  if (ins_class.empty()) {
    product_class = {ProductClass::kFuture, ProductClass::kCont, ProductClass::kIndex};
  } else {
    product_class.push_back(GetProduct(ins_class));
  }

  // 订阅指定合约.
  SubscribleInstrumens("", product_id, exchange_id, product_class, expired, has_night);
  // 查询指定视图.
  auto view = m_db_root->CreateView<Instrument>([=](std::shared_ptr<Instrument> ins) {
    if (!ins_class.empty() && ins->product_class != GetProduct(ins_class))
      return false;

    if (!exchange_id.empty() && ins->exchange_id != exchange_id)
      return false;

    if (!expired.is_none() && ins->expired != expired.cast<bool>())
      return false;

    bool cond = true;
    if (!product_id.empty()) {
      // 主连和指数 product_id 信息采用 instrument_id 进行比较.
      if (ins->product_class == ProductClass::kIndex || ins->product_class == ProductClass::kCont) {
        cond = cond && ins->instrument_id.substr(ins->instrument_id.find(".") + 1) == product_id;
      } else {
        cond = cond && ins->product_id == product_id;
      }
    }

    if (!has_night.is_none())
      cond = cond && (has_night.cast<bool>() ? !ins->trading_time.night.empty() : ins->trading_time.night.empty());

    return cond;
  });

  std::vector<std::string> symbols = {};
  std::transform(view->GetNodes().begin(), view->GetNodes().end(), back_inserter(symbols), RetrieveKey());

  return symbols;
};

std::vector<std::string> TqPythonApi::QueryContQuotes(
  const std::string& exchange_id, const std::string& product_id, py::object& has_night) {
  // 订阅指定合约.
  SubscribleInstrumens("", product_id, "", {ProductClass::kCont, ProductClass::kFuture}, py::none(), has_night);

  // 筛选符合条件的视图
  auto view = m_db_root->CreateView<Instrument>([=](std::shared_ptr<Instrument> ins) {
    if (ins->product_class != ProductClass::kCont)
      return false;
    if (!exchange_id.empty() && ins->underlying_pointer.node->Snap()->exchange_id != exchange_id)
      return false;
    if (!product_id.empty() && ins->instrument_id.substr(ins->instrument_id.find(".") + 1) != product_id)
      return false;
    if (!has_night.is_none() && has_night.cast<bool>() != !ins->trading_time.night.empty())
      return false;
    return true;
  });

  std::vector<std::string> symbols = {};
  for (auto& kv : view->GetNodes()) {
    symbols.push_back(kv.second->Snap()->underlying_pointer.key);
  }

  return symbols;
}

std::vector<std::string> TqPythonApi::QueryOptions(const std::string& underlying_symbol,
  const std::string& option_class, int exercise_year, int exercise_month, double strike_price, py::object& expired,
  py::object& has_A) {
  // 订阅指定合约.
  SubscribleOptions(underlying_symbol);
  auto m = m_db_root->CreateView<Instrument>([=](std::shared_ptr<Instrument> ins) {
    if (ins->underlying_pointer.key.empty() || ins->product_class != ProductClass::kOption) {
      return false;
    }

    if (!underlying_symbol.empty() && ins->underlying_pointer.key != underlying_symbol) {
      return false;
    }

    if (!option_class.empty() && ins->option_class != GetOptionClass(option_class)) {
      return false;
    }

    int ins_exercise_year = std::stoi(ins->last_exercise_day_str.substr(0, 4).c_str());
    if (exercise_year && ins_exercise_year != exercise_year) {
      return false;
    }

    int ins_exercise_month = std::stoi(ins->last_exercise_day_str.substr(4, 2).c_str());
    if (exercise_month && ins_exercise_month != exercise_month) {
      return false;
    }

    if (!DoubleEqual(strike_price, 0.0) && !DoubleEqual(ins->strike_price, strike_price)) {
      return false;
    }

    if (!expired.is_none() && ins->expired != expired.cast<bool>()) {
      return false;
    }

    bool cond = true;
    if (!has_A.is_none()) {
      cond = cond && has_A.cast<bool>() ? ins->english_name.find('A') != std::string::npos
                                        : ins->english_name.find('A') == std::string::npos;
    }

    return cond;
  });

  std::vector<std::string> symbols = {};
  for (auto& kv : m->GetNodes()) {
    symbols.push_back(kv.first);
  }

  return symbols;
}

bool TqPythonApi::SubscribleInstrumens(const std::string& symbol, const std::string& product_id,
  const std::string& exchange_id, std::vector<ProductClass> product_class, py::object include_expired,
  py::object has_night) {
  auto req = std::make_shared<md::SubscribeObjectInfo>();
  req->subscribe_id = std::to_string(random());

  if (!product_class.empty())
    req->product_class_filter = product_class;

  if (!symbol.empty())
    req->instrument_id.push_back(symbol);

  if (!exchange_id.empty())
    req->exchange_id.push_back(exchange_id);

  if (!product_id.empty())
    req->product_id.push_back(product_id);

  if (include_expired.is_none()) {
    req->expired_type = ExpiredType::kBoth;
  } else {
    req->expired_type = include_expired.cast<bool>() ? ExpiredType::kBoth : ExpiredType::kNotExpired;
  }

  if (!has_night.is_none())
    req->has_night = has_night.cast<bool>() ? HasNight::kHasNight : HasNight::kHasNoNight;

  req->timestamp = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : -1;
  TqSyncRequest(m_api, req);
  if (req->result_code) {
    logger.Error("合约信息订阅失败, " + req->result_msg);
    return false;
  }
  return true;
}

bool TqPythonApi::SubscribleOptions(const std::string& underlying_symbol) {
  auto req = std::make_shared<md::SubscribeOptionsByUnderlyingSymbol>();
  req->subscribe_id = std::to_string(random());
  req->symbol = {underlying_symbol};
  req->timestamp = m_is_backtest ? m_options.backtest_service->GetCurrentDateTime() : -1;
  TqSyncRequest(m_api, req);
  if (req->result_code != 0) {
    logger.Error("合约信息订阅失败, " + req->result_msg);
    return false;
  }
  return true;
}

std::shared_ptr<TradingStatus> TqPythonApi::GetTradingStatus(const std::string& symbol) {
  m_trading_status_worker->ConnectServer()->SubInstruments(symbol);

  RunUntilReady(m_api, [&]() {
    m_trading_status_worker->RunOnce();
    return !m_trading_status_worker->m_trading_status[symbol]->status.empty();
  });

  return m_trading_status_worker->m_trading_status[symbol];
}

std::shared_ptr<extension::TargetPosAgent> TqPythonApi::GetTargetPosAgent(const std::string& symbol,
  const std::string& price, const std::string& priority, int unit_id, const py::object& price_func) {
  auto trading_unit = GetCurrentUnitID(unit_id);
  auto key = symbol + "-" + price + "-" + priority + "-" + std::to_string(trading_unit);

  if (m_target_pos_task_map.find(key) == m_target_pos_task_map.end()) {
    EnsureInsValid(symbol);

    if (price_func.is_none()) {
      m_target_pos_task_map[key] = TargetPosAgent::Create(m_api, m_user_key, symbol, trading_unit, price, priority);
    } else {
      m_target_pos_task_map[key] = TargetPosAgent::Create(
        m_api, m_user_key, symbol, trading_unit, price, priority, [price_func](const future::Direction& direction) {
          std::string dir = direction == future::Direction::kBuy ? "BUY" : "SELL";
          return price_func(dir).cast<double>();
        });
    }
  }

  return m_target_pos_task_map[key];
}
