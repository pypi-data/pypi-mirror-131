#include "web_helper.h"

#include <uwebsockets/App.h>
#include <csignal>
#include <atomic>

#include "AsyncFileReader.h"
#include "AsyncFileStreamer.h"
#include "Middleware.h"

std::function<void(int)> ShutDownServerHandle;

uWS::App *globalApp;
ThreadsafeQueue<WebData> global_queue;
std::atomic<bool> send_finished(false);
std::atomic<bool> has_peek_message(false);

void ShutDownServer(int signal) {
  ShutDownServerHandle(signal);
  if (globalApp) {
    delete globalApp;
    globalApp = nullptr;
  }
}

CWebHelper::CWebHelper(
  std::shared_ptr<TqApi> api, const std::string &broker_id, const std::string &account_id, const std::string &user_key)
  : m_api(api)
  , m_broker_id(broker_id)
  , m_account_id(account_id)
  , m_user_key(user_key)
  , m_has_shutdown(false) {
  // 获取被执行的 python 文件信息, 用于 web_gui 展示
  auto sys = py::module::import("sys");
  auto os = py::module::import("os");
  auto py_file = sys.attr("argv").attr("__getitem__")(0);
  m_file_path = os.attr("path").attr("abspath")(py_file).cast<std::string>();
  m_file_name = os.attr("path").attr("basename")(py_file).cast<std::string>();

  // 初始化交易节点视图
  InitTradeView();
}

CWebHelper::~CWebHelper() {
  m_thread.join();
}

CWebHelper &CWebHelper::InitTradeView() {
  // 初始化委托视图
  m_orders_view = m_api->DataDb()->CreateView<Order>(
    [=](std::shared_ptr<Order> content) {
      return content->user_key == m_user_key;
    },
    [&](std::shared_ptr<Order> content) {
      return content->order_id;
    });
  // 初始化成交视图
  m_trades_views = m_api->DataDb()->CreateView<Trade>(
    [=](std::shared_ptr<Trade> content) {
      return content->user_key == m_user_key;
    },
    [&](std::shared_ptr<Trade> content) {
      return content->exchange_trade_id + "|" + content->exchange_order_id;
    });
  // 初始化持仓视图
  m_positions_views = m_api->DataDb()->CreateView<Position>(
    [=](std::shared_ptr<Position> content) {
      return content->user_key == m_user_key;
    },
    [&](std::shared_ptr<Position> content) {
      return content->symbol();
    });
  return *this;
}

std::tuple<std::string, int, std::string> CWebHelper::ParseUrl(const std::string &url) {
  int port = 9001;
  std::string host = "0.0.0.0";
  std::string readable_url = "http://127.0.0.1:9001";

  if (url.compare("True") != 0) {
    std::regex regex("((http)://([^/ :]+))*:?([^/ ]*)");
    std::smatch match;
    std::regex_search(url, match, regex);

    host = std::string(match[3]);
    port = atoi(std::string(match[4]).c_str());
    readable_url = url;

    if (host.empty()) {
      host = "0.0.0.0";
      readable_url = "http://127.0.0.1:" + std::string(match[4]);
    }
  }

  return {host, port, readable_url};
}

CWebHelper &CWebHelper::SetBacktest(std::shared_ptr<BackTestService> backtest) {
  if (backtest != nullptr) {
    m_is_backtest = true;
    m_backtest = backtest;
  }

  return *this;
}

bool CWebHelper::Run(const std::string &url) {
  auto [host, port, readable_url] = ParseUrl(url);

  std::promise<int> thread_init_success;
  std::future<int> thread_init_future = thread_init_success.get_future();

  m_thread = std::thread(
    [&](std::promise<int> init_success) {
      std::string web_path = std::getenv("TQSDK2_WEB_PATH");
      web_path = web_path.empty() ? "./web" : web_path;
      AsyncFileStreamer asyncFileStreamer(web_path);
      struct PerSocketData {};
      auto app = uWS::App();
      struct us_listen_socket_t *global_listen_socket;

      std::signal(SIGINT, ShutDownServer);

      ShutDownServerHandle = [&](int signal) {
        if (global_listen_socket) {
          us_listen_socket_close(0, global_listen_socket);
          global_listen_socket = nullptr;
        }
        std::unique_lock<std::mutex> lck(m_mtx_shutdown);
        m_has_shutdown = true;
        m_cv_shutdown.notify_all();
      };

      app.get("/", [&asyncFileStreamer](auto *res, auto *req) {
        serveFile(res, req);
        asyncFileStreamer.streamFile(res, "/index.html");
      });
      app.get("/index.html", [&asyncFileStreamer](auto *res, auto *req) {
        serveFile(res, req);
        asyncFileStreamer.streamFile(res, "/index.html");
      });
      app.get("/web/*", [&asyncFileStreamer](auto *res, auto *req) {
        serveFile(res, req);
        asyncFileStreamer.streamFile(res, req->getUrl().substr(4));
      });
      app.get("/url", [&asyncFileStreamer](auto *res, auto *req) {
        // 行情地址和合约服务器地址硬编码
        res->writeHeader("Access-Control-Allow-Origin", "*")
          ->end(
            "{\"ins_url\": \"https://openmd.shinnytech.com/t/md/symbols/latest.json\", \"md_url\": "
            "\"wss://api.shinnytech.com/t/nfmd/front/mobile\"}");
      });

      auto ws_behavior = uWS::App::WebSocketBehavior<PerSocketData>();
      ws_behavior.compression = uWS::DEDICATED_COMPRESSOR_3KB;
      ws_behavior.maxPayloadLength = 16 * 1024 * 1024;
      ws_behavior.idleTimeout = 60;
      ws_behavior.maxBackpressure = 1 * 1024 * 1024;
      ws_behavior.upgrade = nullptr;

      ws_behavior.open = [&](auto *ws) {
        // 连接建立后, 获取最新业务截面, 同时订阅主题
        auto diff = GetLatestDiff();
        ws->send(diff.ToString(), uWS::OpCode::TEXT);
        ws->subscribe("tqsdk2_web_broadcast");
      };

      ws_behavior.message = [&](auto *ws, std::string_view message, uWS::OpCode opCode) {
        has_peek_message.store(true);
      };

      app.ws<PerSocketData>("/*", std::move(ws_behavior)).listen(host, port, [&](auto *listen_socket) {
        global_listen_socket = listen_socket;
        if (listen_socket) {
          py::print(" INFO - 您可以访问 ", readable_url, " 查看策略绘制出的 K 线图形.");
          init_success.set_value(1);
        } else {
          py::print(" ERROR - Web GUI 启动失败, 请检查参数是否正确或端口是否被占用.");
          init_success.set_value(0);
        }
      });

      // 每间隔 500 毫秒广播一次
      struct us_loop_t *loop = (struct us_loop_t *)uWS::Loop::get();
      struct us_timer_t *delayTimer = us_create_timer(loop, 0, 0);

      us_timer_set(
        delayTimer,
        [](struct us_timer_t *t) {
          auto elem = global_queue.pop();
          if (elem) {
            WebData data = *elem;
            globalApp->publish("tqsdk2_web_broadcast", data.ToString(), uWS::OpCode::TEXT, true);
            has_peek_message.store(false);
            // 当回测状态为 结束时，发送完成最后一个数据包后关闭推送.
            if (data.diff_status == DiffStatus::kFinished) {
              us_timer_close(t);
              send_finished.store(true);
            }
          }
        },
        50, 50);
      globalApp = &app;
      app.run();
    },
    std::move(thread_init_success));

  // 等待server线程启动完毕
  return thread_init_future.get();
}

int CWebHelper::RunOnce() {
  // 获取最新的业务截面
  auto data = GetLatestDiff();
  // 若业务信息截面发生了变化, 则将该截面放入队列等待广播至所有 web client.
  if (data.diff_status != DiffStatus::kUnChanged) {
    global_queue.push(data);
  }

  return global_queue.size();
}

void CWebHelper::TearDown() {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  while (!(send_finished.load() && has_peek_message.load())) {
    std::this_thread::sleep_for(std::chrono::milliseconds(5000));

    RunOnce();

    if (std::chrono::steady_clock::now() - start > std::chrono::seconds(10))
      break;
  }
  py::print("----------- Backtest finished, press [Ctrl + C] to exit. -----------");
}

void CWebHelper::WaitTearDown() {
  // 等待服务关闭信号 Ctrl+C
  py::print("----------- Backtest finished, press [Ctrl + C] to exit. -----------");
  std::unique_lock<std::mutex> lck(m_mtx_shutdown);
  while (!m_has_shutdown)
    m_cv_shutdown.wait(lck);
}

CWebHelper &CWebHelper::SetReportResult(std::shared_ptr<ProfitReport> report) {
  m_report = report;
  return *this;
}

CWebHelper &CWebHelper::SetSubscribles(std::shared_ptr<Subscribed> subs) {
  m_sub_instruments = subs;
  return *this;
}

WebData CWebHelper::GetLatestDiff() {
  WebData data(m_user_key);
  data.action->mode = m_is_backtest ? "backtest" : "run";
  data.action->td_url_status = true;
  data.action->account_id = m_account_id;
  data.action->account_key = m_user_key;
  data.action->broker_id = m_broker_id;
  data.action->file_name = m_file_name;
  data.action->file_path = m_file_path;

  // 业务截面未发生变化则直接返回
  auto root = m_api->DataDb();
  data.diff_status = DiffStatus::kChanged;

  // 更新回测时间信息
  if (m_is_backtest) {
    data.tqsdk_backtest->start_dt = m_backtest->m_start_dt;
    data.tqsdk_backtest->end_dt = m_backtest->m_end_dt;
    data.tqsdk_backtest->current_dt = m_backtest->GetCurrentDateTime();
  }

  //订阅合约信息
  data.subscribed.push_back(m_sub_instruments);

  //交易数据
  data.trade[m_user_key]->accounts["CNY"]->node = root->GetNode<Account>(m_user_key + "|0|CNY");
  data.trade[m_user_key]->orders = m_orders_view->GetNodes();
  data.trade[m_user_key]->trades = m_trades_views->GetNodes();
  data.trade[m_user_key]->positions = m_positions_views->GetNodes();

  // 权益变动 snapshot
  auto tm = m_is_backtest ? m_backtest->GetCurrentDateTime() : NowAsEpochNano();
  data.snapshots[std::to_string(tm)] = std::make_shared<WebTrade>();
  data.snapshots[std::to_string(tm)]->accounts = data.trade[m_user_key]->accounts;
  data.snapshots[std::to_string(tm)]->positions = data.trade[m_user_key]->positions;

  // 回测结束统计盈亏报表
  if (m_is_backtest && m_backtest->GetStatus() == fclib::md::BackTestServiceStatus::kStopped) {
    data.trade[m_user_key]->accounts["CNY"]->_tqsdk_stat = m_report;
    data.diff_status = DiffStatus::kFinished;
  }

  return data;
}