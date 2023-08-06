/*******************************************************************************
 * @file obj.cpp
 * @brief api python 对象结构声明
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "obj.h"
#include "field_mapping.h"

std::string GetRepr(std::shared_ptr<InstrumentNode> node) {
  std::stringstream ss;
  ss << "{";
  REPR_FILED(ss, node, exchange_id, exchange_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, instrument_id, instrument_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, last_price, last_price, TQ_NAN, number);
  REPR_FILED(ss, node, ask_price1, ask_price[0], TQ_NAN, number);
  REPR_FILED(ss, node, ask_price2, ask_price[1], TQ_NAN, number);
  REPR_FILED(ss, node, ask_price3, ask_price[2], TQ_NAN, number);
  REPR_FILED(ss, node, ask_price4, ask_price[3], TQ_NAN, number);
  REPR_FILED(ss, node, ask_price5, ask_price[4], TQ_NAN, number);
  REPR_FILED(ss, node, ask_volume1, ask_volume[0], TQ_NAN, number);
  REPR_FILED(ss, node, ask_volume2, ask_volume[1], TQ_NAN, number);
  REPR_FILED(ss, node, ask_volume3, ask_volume[2], TQ_NAN, number);
  REPR_FILED(ss, node, ask_volume4, ask_volume[3], TQ_NAN, number);
  REPR_FILED(ss, node, ask_volume5, ask_volume[4], TQ_NAN, number);
  REPR_FILED(ss, node, bid_price1, bid_price[0], TQ_NAN, number);
  REPR_FILED(ss, node, bid_price2, bid_price[1], TQ_NAN, number);
  REPR_FILED(ss, node, bid_price3, bid_price[2], TQ_NAN, number);
  REPR_FILED(ss, node, bid_price4, bid_price[3], TQ_NAN, number);
  REPR_FILED(ss, node, bid_price5, bid_price[4], TQ_NAN, number);
  REPR_FILED(ss, node, bid_volume1, bid_volume[0], TQ_NAN, number);
  REPR_FILED(ss, node, bid_volume2, bid_volume[1], TQ_NAN, number);
  REPR_FILED(ss, node, bid_volume3, bid_volume[2], TQ_NAN, number);
  REPR_FILED(ss, node, bid_volume4, bid_volume[3], TQ_NAN, number);
  REPR_FILED(ss, node, bid_volume5, bid_volume[4], TQ_NAN, number);
  REPR_FILED(ss, node, highest, highest, TQ_NAN, number);
  REPR_FILED(ss, node, lowest, lowest, TQ_NAN, number);
  REPR_FILED(ss, node, open, open, TQ_NAN, number);
  REPR_FILED(ss, node, close, close, TQ_NAN, number);
  REPR_FILED(ss, node, average, average, TQ_NAN, number);
  REPR_FILED(ss, node, volume, volume, TQ_NAN, number);
  REPR_FILED(ss, node, amount, amount, TQ_NAN, number);
  REPR_FILED(ss, node, open_interest, open_interest, TQ_NAN, number);
  REPR_FILED(ss, node, settlement, settlement, TQ_NAN, number);
  REPR_FILED(ss, node, upper_limit, upper_limit, TQ_NAN, number);
  REPR_FILED(ss, node, lower_limit, lower_limit, TQ_NAN, number);
  ss << "'instrument_name': '" << (node && node->Latest() ? node->Latest()->instrument_name : "");
  ss << "'}";
  return ss.str();
}

std::string GetRepr(std::shared_ptr<PositionNode> node) {
  std::stringstream ss;
  ss << std::fixed;
  ss << "{";
  REPR_FILED(ss, node, exchange_id, exchange_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, instrument_id, instrument_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, pos, volume_net(), 0, number);
  REPR_FILED(ss, node, pos_long_his, subpos_long_spec.volume_his, 0, number);
  REPR_FILED(ss, node, pos_long_today, subpos_long_spec.volume_today, 0, number);
  REPR_FILED(ss, node, pos_short_his, subpos_short_spec.volume_his, 0, number);
  REPR_FILED(ss, node, pos_short_today, subpos_short_spec.volume_today, 0, number);
  REPR_FILED(ss, node, volume_long_today, subpos_long_spec.volume_today, 0, number);
  REPR_FILED(ss, node, volume_long_his, subpos_long_spec.volume_his, 0, number);
  REPR_FILED(ss, node, volume_long_frozen_today, subpos_long_spec.volume_today_frozen, 0, number);
  REPR_FILED(ss, node, volume_long_frozen_his, subpos_long_spec.volume_his_frozen, 0, number);
  REPR_FILED(ss, node, volume_short_today, subpos_short_spec.volume_today, 0, number);
  REPR_FILED(ss, node, volume_short_his, subpos_short_spec.volume_his, 0, number);
  REPR_FILED(ss, node, volume_short_frozen_today, subpos_short_spec.volume_today_frozen, 0, number);
  REPR_FILED(ss, node, volume_short_frozen_his, subpos_short_spec.volume_his_frozen, 0, number);
  REPR_FILED(ss, node, open_price_long, subpos_long_spec.open_price, TQ_NAN, number);
  REPR_FILED(ss, node, open_price_short, subpos_short_spec.open_price, TQ_NAN, number);
  REPR_FILED(ss, node, open_cost_long, subpos_long_spec._open_cost, TQ_NAN, number);
  REPR_FILED(ss, node, open_cost_short, subpos_short_spec._open_cost, TQ_NAN, number);
  REPR_FILED(ss, node, position_price_long, subpos_long_spec.position_price, TQ_NAN, number);
  REPR_FILED(ss, node, position_price_short, subpos_short_spec.position_price, TQ_NAN, number);
  REPR_FILED(ss, node, position_cost_long, subpos_long_spec._position_cost, TQ_NAN, number);
  REPR_FILED(ss, node, position_cost_short, subpos_short_spec._position_cost, TQ_NAN, number);
  REPR_FILED(ss, node, float_profit_long, subpos_long_spec.float_profit, TQ_NAN, number);
  REPR_FILED(ss, node, float_profit_short, subpos_short_spec.float_profit, TQ_NAN, number);
  REPR_FILED(ss, node, position_profit_long, subpos_long_spec.position_profit, TQ_NAN, number);
  REPR_FILED(ss, node, position_profit_short, subpos_short_spec.position_profit, TQ_NAN, number);
  REPR_FILED(ss, node, margin_long, subpos_long_spec.margin, TQ_NAN, number);
  REPR_FILED(ss, node, margin_short, subpos_short_spec.margin, TQ_NAN, number);
  REPR_FILED(ss, node, market_value_long, subpos_long_spec.market_value, TQ_NAN, number);
  REPR_FILED(ss, node, market_value_short, subpos_short_spec.market_value, TQ_NAN, number);
  REPR_FILED(ss, node, pos_long, volume_long(), 0, number);
  REPR_FILED(ss, node, pos_short, volume_short(), 0, number);
  REPR_FILED(ss, node, volume_long, volume_long(), 0, number);
  REPR_FILED(ss, node, volume_short, volume_short(), 0, number);
  ss << "'investor_id': '" << node && node->Latest() ? node->Latest()->investor_id : "";
  ss << "'}";
  return ss.str();
}

std::string GetRepr(std::shared_ptr<AccountNode> node) {
  std::stringstream ss;
  ss << std::fixed;
  ss << "{";
  REPR_FILED(ss, node, currency, currency, "CNY", string);
  REPR_FILED(ss, node, pre_balance, pre_balance, TQ_NAN, number);
  REPR_FILED(ss, node, balance, balance, TQ_NAN, number);
  REPR_FILED(ss, node, available, available, TQ_NAN, number);
  REPR_FILED(ss, node, float_profit, float_profit, TQ_NAN, number);
  REPR_FILED(ss, node, position_profit, position_profit, TQ_NAN, number);
  REPR_FILED(ss, node, close_profit, close_profit, TQ_NAN, number);
  REPR_FILED(ss, node, frozen_margin, frozen_margin, TQ_NAN, number);
  REPR_FILED(ss, node, margin, margin, TQ_NAN, number);
  REPR_FILED(ss, node, frozen_commission, frozen_commission, TQ_NAN, number);
  REPR_FILED(ss, node, commission, commission, TQ_NAN, number);
  REPR_FILED(ss, node, frozen_premium, frozen_premium, TQ_NAN, number);
  REPR_FILED(ss, node, premium, premium, TQ_NAN, number);
  REPR_FILED(ss, node, deposit, deposit, TQ_NAN, number);
  REPR_FILED(ss, node, withdraw, withdraw, TQ_NAN, number);
  REPR_FILED(ss, node, risk_ratio, risk_ratio, TQ_NAN, number);
  REPR_FILED(ss, node, market_value, option_market_value, TQ_NAN, number);
  ss << "'investor_id': '" << node->Latest()->investor_id << "'}";
  return ss.str();
}

std::string GetRepr(std::shared_ptr<OrderNode> node) {
  std::stringstream ss;
  ss << std::fixed;
  ss << "{";
  REPR_FILED(ss, node, order_id, order_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, exchange_order_id, exchange_order_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, exchange_id, exchange_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, instrument_id, instrument_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, volume_orign, volume_orign, TQ_NAN, number);
  REPR_FILED(ss, node, volume_left, volume_left, TQ_NAN, number);
  REPR_FILED(ss, node, limit_price, limit_price, TQ_NAN, number);
  REPR_FILED(ss, node, insert_date_time, insert_date_time, TQ_NAN, number);
  REPR_FILED(ss, node, last_msg, status_msg, TQ_NULL_STR, string);
  ss << "'direction': '" << (node && node->Latest() ? GetDirection(node->Latest()->direction) : "") << "', ";
  ss << "'offset': '" << (node && node->Latest() ? GetOffSet(node->Latest()->offset) : "") << "', ";
  ss << "'price_type': '" << (node && node->Latest() ? GetPriceType(node->Latest()->price_type) : "") << "', ";
  ss << "'volume_condition': '" << (node && node->Latest() ? GetVolumeCondition(node->Latest()->volume_condition) : "")
     << "', ";
  ss << "'time_condition': '" << (node && node->Latest() ? GetTimeCondition(node->Latest()->time_condition) : "")
     << "', ";
  ss << "'status': '" << (node && node->Latest() ? GetStatus(node) : "") << "'}";
  return ss.str();
}

std::string GetRepr(std::shared_ptr<TradeNode> node) {
  std::stringstream ss;
  ss << std::fixed;
  ss << "{";
  REPR_FILED(ss, node, order_id, order_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, trade_id, exchange_trade_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, exchange_trade_id, exchange_trade_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, exchange_id, exchange_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, instrument_id, instrument_id, TQ_NULL_STR, string);
  REPR_FILED(ss, node, price, price, TQ_NAN, number);
  REPR_FILED(ss, node, volume, volume, TQ_NAN, number);
  REPR_FILED(ss, node, trade_date_time, trade_date_time, TQ_NAN, number);
  ss << "'direction': '" << GetDirection(node->Latest()->direction) << "', ";
  ss << "'offset': '" << GetOffSet(node->Latest()->offset) << "'}";
  return ss.str();
}

std::string GetInsClass(md::ProductClass product_class) {
  switch (product_class) {
    case md::ProductClass::kFuture: return "FUTURE";   /**< 合约类型 - 期货 */
    case md::ProductClass::kCont: return "CONT";       /**< 合约类型 - 主连 */
    case md::ProductClass::kCombine: return "COMBINE"; /**< 合约类型 - 组合 */
    case md::ProductClass::kIndex: return "INDEX";     /**< 合约类型 - 指数 */
    case md::ProductClass::kOption: return "OPTION";   /**< 合约类型 - 期权 */
    case md::ProductClass::kStock: return "STOCK";     /**< 合约类型 - 股票 */
    default: return "Unknown ProductClass_Type";
  }
}

std::string GetPriceType(future::PriceType p) {
  switch (p) {
    case fclib::future::PriceType::kLimit: return "LIMIT";
    case fclib::future::PriceType::kAny: return "ANY";
    case fclib::future::PriceType::kBest: return "BEST";
    case fclib::future::PriceType::kFiveLevel: return "FIVELEVEL";
    default: return "Unknown PRICE_TYPE";
  }
}

std::string GetVolumeCondition(future::OrderVolumeCondition o) {
  std::string volume_condition;
  switch (o) {
    case fclib::future::OrderVolumeCondition::kAny: return "ANY";
    case fclib::future::OrderVolumeCondition::kMin: return "MIN";
    case fclib::future::OrderVolumeCondition::kAll: return "ALL";
    default: return "Unknown ORDERVOLUMECONDITION_TYPE";
  }
}

std::string GetTimeCondition(future::OrderTimeCondition o) {
  switch (o) {
    case fclib::future::OrderTimeCondition::kIoc: return "IOC";
    case fclib::future::OrderTimeCondition::kGfs: return "GFS";
    case fclib::future::OrderTimeCondition::kGfd: return "GFD";
    case fclib::future::OrderTimeCondition::kGtd: return "GTD";
    case fclib::future::OrderTimeCondition::kGtc: return "GTC";
    case fclib::future::OrderTimeCondition::kGfa: return "GFA";
    default: return "Unknown ORDERTIMECONDITION_TYPE";
  }
}

std::string GetStatus(std::shared_ptr<OrderNode> node, bool is_historical) {
  if (is_historical && node->Historical() == nullptr)
    return std::string("ALIVE");

  auto content = is_historical && node->Historical() ? node->Historical() : node->Latest();
  switch (content->status) {
    case fclib::future::OrderStatus::kAlive: return "ALIVE";
    case fclib::future::OrderStatus::kDead: return "FINISHED";
    default: return "Unknown ORDER_STATUS_TYPE";
  }
}
