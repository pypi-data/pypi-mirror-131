#include "web_data.h"

WebData::WebData(const std::string& account_key) {
  // 基础信息
  action = std::make_shared<Action>();
  // 初始化交易数据.
  trade[account_key] = std::make_shared<WebTrade>();
  tqsdk_backtest = std::make_shared<WebBacktest>();
  diff_status = DiffStatus::kUnChanged;
}

std::string WebData::ToString() {
  RtnData diff;
  diff.aid = "rtn_data";
  diff.data.push_back(*this);

  WebDataSerializer s;
  s.FromVar(diff);
  rapidjson::StringBuffer sb;
  rapidjson::Writer<rapidjson::StringBuffer> writer(sb);
  s.m_doc->Accept(writer);
  return std::string(sb.GetString());
}