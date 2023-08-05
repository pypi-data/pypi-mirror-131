/*******************************************************************************
 * @file filed_mapping.cpp
 * @brief tqsdk2 和 fclib 部分字段映射声明文件
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "field_mapping.h"

void FieldSerializer::DefineStruct(security::Account& d) {
  AddItem(d.user_id, "user_id");
  AddItem("CNY", "currency");
  AddItem(d.available, "available");
  AddItem(d.available_his, "available_his");
  AddItem(d.buy_frozen_balance, "buy_frozen_balance");
  AddItem(d.buy_frozen_fee, "buy_frozen_fee");
  AddItem(d.buy_balance_today, "buy_balance_today");
  AddItem(d.buy_fee_today, "buy_fee_today");
  AddItem(d.sell_balance_today, "sell_balance_today");
  AddItem(d.sell_fee_today, "sell_fee_today");
  AddItem(d.deposit, "deposit");
  AddItem(d.withdraw, "withdraw");
  AddItem(d.drawable, "drawable");
  AddItem(d.market_value, "market_value");
  AddItem(d.asset, "asset");
  AddItem(d.asset_his, "asset_his");
  AddItem(d.dividend_balance_today, "dividend_balance_today");
  AddItem(d.cost, "cost");
  AddItem(d.hold_profit, "hold_profit");
  AddItem(d.float_profit_today, "float_profit_today");
  AddItem(d.real_profit_today, "real_profit_today");
  AddItem(d.profit_today, "profit_today");
  AddItem(d.profit_rate_today, "profit_rate_today");
}

void FieldSerializer::DefineStruct(security::Position& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.create_date, "create_date");
  AddItem(d.volume, "volume");
  AddItem(d.last_price, "last_price");
  AddItem(d.buy_volume_today, "buy_volume_today");
  AddItem(d.buy_balance_today, "buy_balance_today");
  AddItem(d.buy_fee_today, "buy_fee_today");
  AddItem(d.sell_volume_today, "sell_volume_today");
  AddItem(d.sell_balance_today, "sell_balance_today");
  AddItem(d.sell_fee_today, "sell_fee_today");
  AddItem(d.shared_volume_today, "shared_volume_today");
  AddItem(d.devidend_balance_today, "devidend_balance_today");
  AddItem(d.cost, "cost");
  AddItem(d.market_value, "market_value");
  AddItem(d.float_profit_today, "float_profit_today");
  AddItem(d.real_profit_today, "real_profit_today");
  AddItem(d.profit_today, "profit_today");
  AddItem(d.profit_rate_today, "profit_rate_today");
  AddItem(d.hold_profit, "hold_profit");
  AddItem(d.real_profit_total, "real_profit_total");
  AddItem(d.profit_total, "profit_total");
  AddItem(d.profit_rate_total, "profit_rate_total");
}

void FieldSerializer::DefineStruct(security::Order& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.order_id, "order_id");
  AddItem(d.volume_orign, "volume_orign");
  AddItem(d.volume_left, "volume_left");
  AddItem(d.limit_price, "limit_price");
  AddItem(d.insert_date_time, "insert_date_time");
  AddItem(d.status_msg, "status_msg");
  AddItemEnum(d.direction, ("direction"),
    {
      {security::Direction::kBuy, ("BUY")},
      {security::Direction::kSell, ("SELL")},
    });
  AddItemEnum(d.price_type, ("price_type"),
    {
      {security::PriceType::kLimit, ("LIMIT")},
      {security::PriceType::kAny, ("ANY")},
    });
  AddItemEnum(d.status, ("status"),
    {
      {security::OrderStatus::kAlive, ("ALIVE")},
      {security::OrderStatus::kDead, ("FINISHED")},
    });
}

void FieldSerializer::DefineStruct(security::Trade& d) {
  AddItem(d.user_id, "user_id");
  AddItem(d.exchange_id, "exchange_id");
  AddItem(d.instrument_id, "instrument_id");
  AddItem(d.trade_id, "trade_id");
  AddItem(d.order_id, "order_id");
  AddItem(d.exchange_trade_id, "exchange_trade_id");
  AddItem(d.price, "price");
  AddItem(d.volume, "volume");
  //AddItem(d.balance(), "balance");
  AddItem(d.fee, "fee");
  AddItemEnum(d.direction, ("direction"),
    {
      {security::Direction::kBuy, ("BUY")},
      {security::Direction::kSell, ("SELL")},
    });
  AddItem(d.trade_date_time, "trade_date_time");
}

Direction GetDirection(const std::string& direction) {
  if (!direction.compare("BUY")) {
    return Direction::kBuy;
  } else if (!direction.compare("SELL")) {
    return Direction::kSell;
  } else {
    throw std::invalid_argument("下单方向 " + direction + " 错误, 请检查 direction 参数是否填写正确.");
  }
}

std::string GetDirection(Direction d) {
  switch (d) {
    case Direction::kBuy: return "BUY";
    case Direction::kSell: return "SELL";
    default: return "Unknown DIRECTION_TYPE";
  }
}

Offset GetOffSet(const std::string& offset) {
  if (!offset.compare("OPEN") || !offset.compare("kOpen")) {
    return Offset::kOpen;
  } else if (!offset.compare("CLOSE") || !offset.compare("kClose")) {
    return Offset::kClose;
  } else if (!offset.compare("CLOSETODAY") || !offset.compare("kCloseToday")) {
    return Offset::kCloseToday;
  } else {
    throw std::invalid_argument("开平标志 " + offset + " 错误, 请检查 offset 是否填写正确.");
  }
}

std::string GetOffSet(Offset o) {
  switch (o) {
    case Offset::kOpen: return "OPEN";
    case Offset::kClose: return "CLOSE";
    case Offset::kCloseToday: return "CLOSETODAY";
    default: return "Unknown OFFSET_TYPE";
  }
}

ProductClass GetProduct(const std::string& product_class) {
  if (!product_class.compare("CONT")) {
    return ProductClass::kCont;
  } else if (!product_class.compare("FUTURE")) {
    return ProductClass::kFuture;
  } else if (!product_class.compare("OPTION")) {
    return ProductClass::kOption;
  } else if (!product_class.compare("COMBINE")) {
    return ProductClass::kCombine;
  } else if (!product_class.compare("INDEX")) {
    return ProductClass::kIndex;
  } else if (!product_class.compare("STOCK")) {
    return ProductClass::kStock;
  } else if (!product_class.compare("FUND")) {
    return ProductClass::kFund;
  } else {
    throw std::invalid_argument("合约类型 " + product_class + " 错误, 请检查 ins_class 参数是否填写正确.");
  }
}

OptionClass GetOptionClass(const std::string& option_class) {
  if (!option_class.compare("CALL")) {
    return OptionClass::kCall;
  } else if (!option_class.compare("PUT")) {
    return OptionClass::kPut;
  } else {
    throw std::invalid_argument("期权类型 " + option_class + " 错误, 请检查 option_class 参数是否填写正确.");
  }
}

std::string GetTradeStatus(TradeStatus ts) {
  switch (ts) {
    case TradeStatus::kBeforeTrading: return "BEFORETRADING";
    case TradeStatus::kAuctionOrdering: return "AUCTIONORDERING";
    case TradeStatus::kAuctionBalance: return "AUCTIONBALANCE";
    case TradeStatus::kAuctionMatch: return "AUCTIONMATCH";
    case TradeStatus::kContinous: return "CONTINOUS";
    case TradeStatus::kNoTrading: return "NOTRADING";
    case TradeStatus::kClosed: return "CLOSED";
    default: return "";
  }
}