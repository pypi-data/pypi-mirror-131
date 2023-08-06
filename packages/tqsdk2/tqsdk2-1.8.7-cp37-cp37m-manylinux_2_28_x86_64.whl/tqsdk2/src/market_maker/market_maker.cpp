/*******************************************************************************
 * @file market_maker.cpp
 * @brief 做市模块实现
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "market_maker.h"
#include "../api_impl.h"

TqMarketMaker::TqMarketMaker(py::object api, const std::string& symbol) {
  m_api = api.cast<TqPythonApi&>().GetApi();
  m_user_key = api.cast<TqPythonApi&>().GetUserKey();
  m_market_maker = fclib::extension::MarketMakerStrategy::Create(m_api);
  m_market_maker->m_ins_node = api.cast<TqPythonApi&>().SubscribeQuote(symbol);

  if (!m_market_maker->m_ins_node) {
    m_api->CleanUp();
    std::string msg = "合约代码 " + symbol + " 不存在, 请检查合约代码是否填写正确.";
    throw std::invalid_argument(msg.c_str());
  }

  // 设置默认值
  m_market_maker->m_net_position_limit = 100;
  m_market_maker->m_close_profit_limit = 10000;

  // Hack: 启用 做市策略时, 提前设置下单手数，否则无法创建两对双边挂单
  m_market_maker->m_quote_volume_2 = 1;
  m_market_maker->m_quote_spread_2 = 1;
  m_market_maker->Start(m_user_key);
  m_market_maker->m_quote_volume_2 = 0;
  m_market_maker->m_quote_spread_2 = 0;

  api.cast<TqPythonApi&>().AddMarketMakerStrategy(m_market_maker);
}

TqMarketMaker::~TqMarketMaker() {}

void TqMarketMaker::SetMarketMakerConfig(py::kwargs kwargs) {
  if (kwargs.contains("quote_spread")) {
    m_market_maker->m_quote_spread = kwargs["quote_spread"].cast<int>();
  }
  if (kwargs.contains("quote_volume")) {
    m_market_maker->m_quote_volume = kwargs["quote_volume"].cast<int>();
  }
  if (kwargs.contains("quote_spread_2")) {
    m_market_maker->m_quote_spread_2 = kwargs["quote_spread_2"].cast<int>();
  }
  if (kwargs.contains("quote_volume_2")) {
    m_market_maker->m_quote_volume_2 = kwargs["quote_volume_2"].cast<int>();
  }
  if (kwargs.contains("min_position_volume")) {
    m_market_maker->m_min_position_volume = kwargs["min_position_volume"].cast<int>();  //最小持仓数量限制
  }
  if (kwargs.contains("bid_min_volume")) {
    m_market_maker->m_bid_min_volume = kwargs["bid_min_volume"].cast<int>();  //最小买量限制
  }
  if (kwargs.contains("ask_min_volume")) {
    m_market_maker->m_ask_min_volume = kwargs["ask_min_volume"].cast<int>();  //最小卖量限制
  }
  if (kwargs.contains("use_quote_command")) {
    m_market_maker->m_use_quote_command = kwargs["use_quote_command"].cast<bool>();  //使用做市报价指令
  }
  if (kwargs.contains("spread_limit")) {
    m_market_maker->m_spread_limit = kwargs["spread_limit"].cast<int>();
  }
  if (kwargs.contains("price_limit")) {
    m_market_maker->m_price_limit = kwargs["price_limit"].cast<int>();
  }
  if (kwargs.contains("time_range")) {
    if (!py::isinstance<py::list>(kwargs["time_range"])) {
      throw std::invalid_argument("做市时间段格式错误.");
    }

    auto time_range = kwargs["time_range"].cast<py::list>();

    for (py::handle tr : time_range) {
      auto tr_tuple = tr.cast<py::tuple>();
      if (tr_tuple.size() != 2)
        throw std::invalid_argument("做市时间段格式错误.");

      int start_dt = atoi(tr_tuple[0].cast<std::string>().c_str());
      int end_dt = atoi(tr_tuple[1].cast<std::string>().c_str());
      m_market_maker->m_time_range[start_dt] = true;
      m_market_maker->m_time_range[end_dt] = false;
    }
  }
  if (kwargs.contains("net_position_limit")) {
    m_market_maker->m_net_position_limit = kwargs["net_position_limit"].cast<int>();
  }
  if (kwargs.contains("close_profit_limit")) {
    m_market_maker->m_close_profit_limit = kwargs["close_profit_limit"].cast<double>();
  }
  if (kwargs.contains("move_speed_limit")) {
    m_market_maker->m_move_speed_limit = kwargs["move_speed_limit"].cast<double>();
  }
  if (kwargs.contains("pause_seconds_when_trade")) {
    m_market_maker->m_pause_seconds_when_trade = kwargs["pause_seconds_when_trade"].cast<double>();
  }

  if (kwargs.contains("run_hedge")) {
    m_market_maker->m_require_run_hedge = kwargs["run_hedge"].cast<bool>();
  }
  if (kwargs.contains("hedge_instrument_id")) {
    m_market_maker->m_hedge_instrument_id = kwargs["hedge_instrument_id"].cast<std::string>();
  }
  if (kwargs.contains("hedge_order_max_price_adjust")) {
    m_market_maker->m_hedge_order_max_price_adjust = kwargs["hedge_order_max_price_adjust"].cast<int>();
  }
}

void TqMarketMaker::Stop(const std::string& reason) {
  m_market_maker->Stop(reason);

  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  while (HasAliveOrders()) {
    if (std::chrono::steady_clock::now() - start > std::chrono::seconds(30)) {
      break;
    }
    m_api->RunOnce();
    m_market_maker->RunOnce();
  }
}

std::string TqMarketMaker::GetStatus() {
  if (!m_market_maker->m_running)
    return "NOT_RUNNING";

  return m_market_maker->m_status_msg == "运行中: 做市运行中" ? "RUNNING" : "PAUSE";
}

bool TqMarketMaker::HasAliveOrders() {
  auto orders_node = m_api->DataDb()->GetNodeMap<Order>();
  for (auto [order_id, node] : orders_node) {
    if (node->Snap()->status == fclib::future::OrderStatus::kAlive) {
      return true;
    }
  }

  return false;
}