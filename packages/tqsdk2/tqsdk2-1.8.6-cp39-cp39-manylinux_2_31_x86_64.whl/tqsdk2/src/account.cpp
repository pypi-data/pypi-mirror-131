/*******************************************************************************
 * @file account.cpp
 * @brief TqSDK2 账户实例声明
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "account.h"
#include "DataCollect.h"

TqUser::TqUser() : m_trading_unit(std::make_shared<TradingUnit>()) {}

TqUser& TqUser::Login(std::shared_ptr<TqApi> api) {
  TqSyncRequest(api, m_login_req);
  if (m_login_req->result_code != 0)
    throw std::exception(std::logic_error("用户登录失败, " + m_login_req->result_msg));

  // 确认交易服务器连接完成
  RunUntilReady(api, [&]() -> bool {
    auto login_node = api->DataDb()->GetNode<future::LoginContent>(m_user_key);
    return login_node && login_node->Snap()->account_ready && login_node->Snap()->position_ready;
  });

  return *this;
}

TqUser& TqUser::PostLogin(std::shared_ptr<TqApi> api) {
  return *this;
}

TqUser& TqUser::EnableTradingUnit(int trading_unit) {
  if (trading_unit != ktrade_unit_unset) {
    m_trading_unit->EnableTradingUnit(trading_unit);
  }
  return *this;
}

TqCtp::TqCtp(const std::string& front_url, const std::string& front_broker, const std::string& app_id,
  const std::string& auth_code, const std::string& account_id, const std::string& password, int trading_unit) {
  m_user_key = account_id;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = front_broker;
  m_login_req->broker.ctp_broker_id = front_broker;
  m_login_req->broker.trading_fronts.push_back(front_url);
  m_login_req->broker.product_info = std::string("SHINNY_TQ_1.0");
  m_login_req->broker.app_id = app_id;
  m_login_req->broker.auth_code = auth_code;
  m_login_req->user_id = account_id;
  m_login_req->password = password;
  m_login_req->user_key = m_user_key;
  m_login_req->backend = BackEnd::kCtp;
  // 启用交易单元
  EnableTradingUnit(trading_unit);
}

TqCtp& TqCtp::SetAuth(std::shared_ptr<TqAuth> auth) {
  if (!auth->HasGrant(kAuthCtp)) {
    std::string msg =
      "您的账户暂不支持直连 CTP 柜台，需要购买天勤企业版后使用。升级网址：https ://account.shinnytech.com.";
    throw std::exception(std::logic_error(msg.c_str()));
  }

  //若登录用户不在可交易账户中，则尝试自动绑定.
  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  return *this;
}

TqCtp& TqCtp::PostLogin(std::shared_ptr<TqApi> api) {
  // 确认结算单
  auto req = std::make_shared<ConfirmSettlementInfo>(m_user_key);
  TqSyncRequest(api, req);

  return *this;
}

TqRohon::TqRohon(const std::string& front_url, const std::string& front_broker, const std::string& app_id,
  const std::string& auth_code, const std::string& account_id, const std::string& password, int trading_unit) {
  m_user_key = account_id;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = front_broker;
  m_login_req->broker.ctp_broker_id = front_broker;
  m_login_req->broker.trading_fronts.push_back(front_url);
  m_login_req->broker.product_info = std::string("shinny_tqsdk_01");
  m_login_req->broker.app_id = app_id;
  m_login_req->broker.auth_code = auth_code;
  m_login_req->user_id = account_id;
  m_login_req->password = password;
  m_login_req->user_key = m_user_key;
  m_login_req->backend = BackEnd::kRohon;
  // 启用交易单元
  EnableTradingUnit(trading_unit);
}

TqRohon& TqRohon::SetAuth(std::shared_ptr<TqAuth> auth) {
  if (!auth->HasGrant(kAuthRohon)) {
    std::string msg = "您的账户不支持直连融航资管柜台，需要购买专业版本后使用。升级网址：" + kAccountUrl;
    throw std::exception(std::logic_error(msg.c_str()));
  }

  //若登录用户不在可交易账户中，则尝试自动绑定.
  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  return *this;
}

TqAccount::TqAccount(const std::string& broker_id, const std::string& account_id, const std::string& password,
  int trading_unit, const std::string& _td_url) {
  m_user_key = account_id;
  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = broker_id;
  m_login_req->client_app_id = "SHINNY_TQ_1.0";
  m_login_req->user_id = account_id;
  m_login_req->password = password;
  m_login_req->user_key = m_user_key;
  m_login_req->otg.front_url = _td_url;
  m_login_req->backend = BackEnd::kOtg;

  // 启用交易单元
  EnableTradingUnit(trading_unit);
}

TqAccount& TqAccount::SetAuth(std::shared_ptr<TqAuth> auth) {
  //若登录用户不在可交易账户中，则尝试自动绑定.
  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  // 从 broker list 获取 otg 前置地址.
  if (m_login_req->otg.front_url.empty()) {
    TqHttpClient cli(auth);
    m_login_req->otg.front_url = cli.GetTradeUrl(m_login_req->bid);
  }

  return *this;
}

TqAccount& TqAccount::PostLogin(std::shared_ptr<TqApi> api) {
  // 确认结算单
  auto req = std::make_shared<ConfirmSettlementInfo>(m_user_key);
  TqSyncRequest(api, req);

  return *this;
}

TqSim::TqSim(double init_balance, const std::string& user_key) : init_balance(init_balance) {
  m_user_key = user_key.empty() ? std::to_string((int64_t)this) : user_key;

  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->bid = "TqSim";
  m_login_req->user_id = m_user_key;
  m_login_req->backend = BackEnd::kLocalSim;
}

TqSim& TqSim::SetAuth(std::shared_ptr<TqAuth> auth) {
  return *this;
}

TqSim& TqSim::PostLogin(std::shared_ptr<TqApi> api) {
  m_api = api;
  // TqSim 初始化资金通过出入金实现.
  auto req = std::make_shared<TransferMoney>(m_user_key);
  req->is_deposit = init_balance > kSimInitBalance;
  req->amount = std::abs(init_balance - kSimInitBalance);
  TqSyncRequest(api, req);

  return *this;
}

double TqSim::SetCommission(const std::string& symbol, double commission) {
  auto req = std::make_shared<SetCommissionRate>(m_user_key);
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  req->volume_commission = commission;
  TqSyncRequest(m_api, req);

  return commission;
}

double TqSim::GetCommission(const std::string& symbol) {
  auto instrument_id = symbol.substr(symbol.find(".") + 1);
  auto rate_node = m_api->DataDb()->GetNode<Rate>(m_user_key + "|" + instrument_id);
  if (rate_node && !rate_node->Latest()->commission_rates.empty()
    && !isnan(rate_node->Latest()->commission_rates[0].volume_rate))
    return rate_node->Latest()->commission_rates[0].volume_rate;

  return m_api->DataDb()->GetNode<Instrument>(symbol)->Latest()->commission;
}

double TqSim::SetMargin(const std::string& symbol, double margin) {
  auto req = std::make_shared<SetMarginRate>(m_user_key);
  req->instrument_id = symbol.substr(symbol.find(".") + 1);
  req->volume_margin = margin;
  TqSyncRequest(m_api, req);

  return margin;
}

double TqSim::GetMargin(const std::string& symbol) {
  auto instrument_id = symbol.substr(symbol.find(".") + 1);
  auto rate_node = m_api->DataDb()->GetNode<Rate>(m_user_key + "|" + instrument_id);
  if (rate_node && !rate_node->Latest()->margin_rates.empty()
    && !isnan(rate_node->Latest()->margin_rates[0].volume_rate))
    return rate_node->Latest()->margin_rates[0].volume_rate;

  return m_api->DataDb()->GetNode<Instrument>(symbol)->Latest()->margin;
}

TqKq::TqKq(int trading_unit, const std::string& _td_url) {
  m_td_url = _td_url.empty() ? "wss://otg-sim.shinnytech.com/trade" : _td_url;
  EnableTradingUnit(trading_unit);
}

TqKq& TqKq::SetAuth(std::shared_ptr<TqAuth> auth) {
  m_user_key = auth->GetUserID();

  m_login_req = std::make_shared<future::ReqLogin>(m_user_key);
  m_login_req->otg.front_url = m_td_url;
  m_login_req->bid = "快期模拟";
  m_login_req->backend = BackEnd::kOtg;
  m_login_req->user_key = m_user_key;
  m_login_req->user_id = m_user_key;
  m_login_req->password = m_user_key;

  //若登录用户不在可交易账户中，则尝试自动绑定.
  if (!auth->HasAccountGranted(m_login_req->user_id)) {
    TqHttpClient cli(auth);
    cli.BindAccount(m_login_req->user_id);
  }

  return *this;
}

TqKqStock::TqKqStock(int trading_unit, const std::string& _td_url) {
  m_td_url = _td_url.empty() ? "wss://otg-sim-securities.shinnytech.com/trade" : _td_url;
  EnableTradingUnit(trading_unit);
}

TqKqStock& TqKqStock::SetAuth(std::shared_ptr<TqAuth> auth) {
  m_type = AccountType::kSecurities;
  m_user_key = auth->GetUserID() + "-sim-securities";

  m_login_req = std::make_shared<security::ReqLogin>(m_user_key);
  m_login_req->otg.front_url = m_td_url;
  m_login_req->bid = "快期股票模拟";
  m_login_req->user_key = m_user_key;
  m_login_req->user_id = m_user_key;
  m_login_req->password = m_user_key;
  m_login_req->backend = security::BackEnd::kOtg;

  return *this;
}

TqKqStock& TqKqStock::Login(std::shared_ptr<TqApi> api) {
  TqSyncRequest(api, m_login_req);
  if (m_login_req->result_code != 0)
    throw std::exception(std::logic_error("用户登录失败, " + m_login_req->result_msg));

  RunUntilReady(api, [&]() -> bool {
    auto login_ready = api->DataDb()->GetNode<security::LoginContent>(m_user_key);
    return login_ready && login_ready->Snap()->account_ready && login_ready->Snap()->position_ready;
  });

  return *this;
}

TqKqStock& TqKqStock::PostLogin(std::shared_ptr<TqApi> api) {
  return *this;
}