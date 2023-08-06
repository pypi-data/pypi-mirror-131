/*******************************************************************************
 * @file trading_status.cpp
 * @brief 合约交易状态
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "trading_status.h"
#include <iostream>

TradingStatusWorker::TradingStatusWorker(
  std::shared_ptr<TqApi> api, structlog::Logger& parent_logger, const std::string& access_token)
  : m_api(api)
  , m_has_connected(false)
  , m_logger(parent_logger)
  , m_access_token(access_token) {}

TradingStatusWorker::~TradingStatusWorker() {
  if (m_has_connected) {
    m_ioc.stop();
    m_thread.join();
  }
}

std::shared_ptr<TradingStatusWorker> TradingStatusWorker::ConnectServer() {
  if (m_has_connected)
    return shared_from_this();

  m_ws_client = WebsocketClient::Create(&m_ioc, m_logger);
  m_ws_client->SetHeader("Authorization", "Bearer " + m_access_token);
  m_ws_client->SetHeader("Agent", "tqsdk2");
  m_ws_client
    ->OnSessionBegin([&](std::shared_ptr<WebsocketSession> session) {
      m_has_connected = true;
    })
    ->OnSessionEnd([&](std::shared_ptr<WebsocketSession> session) {})
    ->OnSessionReceivedMessage([&](std::shared_ptr<WebsocketSession> session, const std::string& msg) {
      m_recv_queue.push(msg);
      session->SendTextMsg(R"({"aid":"peek_message"})");
    })
    ->Connect(kTradingStatusServer);

  m_thread = std::thread([&]() {
    m_ioc.run();
  });

  while (!m_has_connected) {
    std::this_thread::yield();
  }

  return shared_from_this();
}

void TradingStatusWorker::RunOnce() {
  //处理接收到的数据包
  std::string msg;
  for (int i = 0; m_recv_queue.pop(msg); i++) {
    ProcessMsg(msg);
  }
}

void TradingStatusWorker::SubInstruments(const std::string& symbol) {
  if (m_trading_status.find(symbol) != m_trading_status.end())
    return;

  m_trading_status[symbol] = std::make_shared<TradingStatus>(symbol);

  std::string ins_list;
  for (auto [s, _] : m_trading_status) {
    ins_list += s + ",";
  }
  ins_list.pop_back();

  auto req = R"({"aid":"subscribe_trading_status", "ins_list":")" + ins_list + R"("})";
  m_ws_client->GetSession()->SendTextMsg(req);
}

void TradingStatusWorker::ProcessMsg(const std::string& msg) {
  TradingStatusRtnDataSerializer ss;
  ss.FromString(msg.c_str());

  if (!ss.m_doc->HasMember("data"))
    return;

  rapidjson::Value& datas = (*ss.m_doc)["data"];
  if (!datas.IsArray())
    return;

  for (auto& data : datas.GetArray()) {
    if (!data.HasMember("trading_status"))
      continue;

    rapidjson::Value& trading_status = data["trading_status"];
    for (auto& s : trading_status.GetObject()) {
      auto symbol = s.name.GetString();
      std::string status = trading_status[symbol]["trade_status"].GetString();
      UpdateStatus(symbol, status);
    }
  }
}

void TradingStatusWorker::UpdateStatus(const std::string& symbol, const std::string& status) {
  if (status == "AUCTIONORDERING") {
    m_trading_status[symbol]->status = "AUCTIONORDERING";
  } else if (status == "CONTINOUS") {
    m_trading_status[symbol]->status = "CONTINOUS";
  } else if (status == "BEFORETRADING") {
    // 合约交易状态为盘前, 但是行情数据提前到来时, 也可以认为进入集合竞价阶段
    auto node = m_api->DataDb()->GetNode<md::Instrument>(symbol);
    if (node && node->Historical()) {
      m_trading_status[symbol]->status = "AUCTIONORDERING";
    } else {
      m_trading_status[symbol]->status = "NOTRADING";
    }
  } else {
    m_trading_status[symbol]->status = "NOTRADING";
  }
}
