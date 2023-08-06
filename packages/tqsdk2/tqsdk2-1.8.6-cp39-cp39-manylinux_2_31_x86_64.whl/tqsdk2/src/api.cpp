/*******************************************************************************
 * @file api.cpp
 * @brief api python 接口
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/operators.h>
#include "api_impl.h"
#include "lib.h"
#include "field_mapping.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using namespace pybind11::literals;

void BindingTqMarketMaker(py::module_& m);
void BindingBacktest(py::module_& m);

/**
 * https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html
 */
PYBIND11_MAKE_OPAQUE(std::map<std::string, std::shared_ptr<OrderNode>>);
PYBIND11_MAKE_OPAQUE(std::map<std::string, std::shared_ptr<TradeNode>>);
PYBIND11_MAKE_OPAQUE(std::map<std::string, std::shared_ptr<PositionNode>>);

PYBIND11_MODULE(tqsdk2, m) {
  m.doc() = R"pbdoc(
        .. currentmodule:: tqsdk2
        .. autosummary::
           :toctree: _generate
           TqApi
           TqAuth
           TqAccount
           TqKq
           TqKqStock
           TqSim
           TqCtp
           TargetPosTask
           TqMarketMaker
    )pbdoc";

  /**
   * 做市商模块绑定
   */
  BindingTqMarketMaker(m);

  /**
   * 回测模块绑定
   */
  BindingBacktest(m);

  py::class_<InstrumentNode, std::shared_ptr<InstrumentNode>>(m, "Quote")
    .FIELD(InstrumentNode, exchange_id, exchange_id, std::string(""), "交易所代码.")
    .FIELD(InstrumentNode, symbol, symbol, std::string(""), "合约代码.")
    .FIELD(InstrumentNode, last_price, last_price, TQ_NAN, "最新价.")
    .FIELD(InstrumentNode, ask_price1, ask_price[0], TQ_NAN, "卖一价.")
    .FIELD(InstrumentNode, ask_price2, ask_price[1], TQ_NAN, "卖二价.")
    .FIELD(InstrumentNode, ask_price3, ask_price[2], TQ_NAN, "卖三价.")
    .FIELD(InstrumentNode, ask_price4, ask_price[3], TQ_NAN, "卖四价.")
    .FIELD(InstrumentNode, ask_price5, ask_price[4], TQ_NAN, "卖五价.")
    .FIELD(InstrumentNode, ask_volume1, ask_volume[0], 0, "卖一量.")
    .FIELD(InstrumentNode, ask_volume2, ask_volume[1], 0, "卖二量.")
    .FIELD(InstrumentNode, ask_volume3, ask_volume[2], 0, "卖三量.")
    .FIELD(InstrumentNode, ask_volume4, ask_volume[3], 0, "卖四量.")
    .FIELD(InstrumentNode, ask_volume5, ask_volume[4], 0, "卖五量.")
    .FIELD(InstrumentNode, bid_price1, bid_price[0], TQ_NAN, "买一价.")
    .FIELD(InstrumentNode, bid_price2, bid_price[1], TQ_NAN, "买二价.")
    .FIELD(InstrumentNode, bid_price3, bid_price[2], TQ_NAN, "买三价.")
    .FIELD(InstrumentNode, bid_price4, bid_price[3], TQ_NAN, "买四价.")
    .FIELD(InstrumentNode, bid_price5, bid_price[4], TQ_NAN, "买五价.")
    .FIELD(InstrumentNode, bid_volume1, bid_volume[0], 0, "买一量.")
    .FIELD(InstrumentNode, bid_volume2, bid_volume[1], 0, "买二量.")
    .FIELD(InstrumentNode, bid_volume3, bid_volume[2], 0, "买三量.")
    .FIELD(InstrumentNode, bid_volume4, bid_volume[3], 0, "买四量.")
    .FIELD(InstrumentNode, bid_volume5, bid_volume[4], 0, "买五量.")
    .FIELD(InstrumentNode, highest, highest, TQ_NAN, "当日最高价.")
    .FIELD(InstrumentNode, lowest, lowest, TQ_NAN, "当日最低价.")
    .FIELD(InstrumentNode, open, open, TQ_NAN, "当日开盘价.")
    .FIELD(InstrumentNode, close, close, TQ_NAN, "当日收盘价.")
    .FIELD(InstrumentNode, average, average, TQ_NAN, "当日均价.")
    .FIELD(InstrumentNode, volume, volume, 0, "成交量.")
    .FIELD(InstrumentNode, amount, amount, TQ_NAN, "成交额.")
    .FIELD(InstrumentNode, open_interest, open_interest, 0, "持仓量.")
    .FIELD(InstrumentNode, settlement, settlement, TQ_NAN, "结算价.")
    .FIELD(InstrumentNode, upper_limit, upper_limit, TQ_NAN, "涨停价.")
    .FIELD(InstrumentNode, lower_limit, lower_limit, TQ_NAN, "跌停价.")
    .FIELD(InstrumentNode, pre_open_interest, pre_open_interest, 0, "昨持仓量.")
    .FIELD(InstrumentNode, pre_settlement, pre_settlement, TQ_NAN, "昨结算价.")
    .FIELD(InstrumentNode, pre_close, pre_close, TQ_NAN, "昨收盘价.")
    .FIELD(InstrumentNode, price_tick, price_tick, TQ_NAN, "合约价格变动单位.")
    .FIELD(InstrumentNode, price_decs, price_decs, 0, "合约价格小数位数.")
    .FIELD(InstrumentNode, volume_multiple, volume_multiple, 0.0, "合约乘数.")
    .FIELD(InstrumentNode, max_limit_order_volume, max_limit_order_volume, 0, "最大限价单手数.")
    .FIELD(InstrumentNode, max_market_order_volume, max_market_order_volume, 0, "最大市价单手数.")
    .FIELD(InstrumentNode, strike_price, strike_price, TQ_NAN, "行权价.")
    .FIELD(InstrumentNode, instrument_id, instrument_id, std::string(""), "合约代码.")
    .FIELD(InstrumentNode, instrument_name, instrument_name, std::string(""), "合约中文名.")
    .FIELD(InstrumentNode, expired, expired, false, "合约是否已下市.")
    .FIELD(InstrumentNode, delivery_year, delivery_year, 0, "期货交割日年份，只对期货品种有效.")
    .FIELD(InstrumentNode, delivery_month, delivery_month, 0, "期货交割日月份，只对期货品种有效.")
    .FIELD(InstrumentNode, product_id, product_id, std::string(""), "品种代码.")
    .FIELD(InstrumentNode, margin, margin, TQ_NAN, "预估单手保证金.")
    .FIELD(InstrumentNode, commission, commission, TQ_NAN, "预估单手手续费.")
    .def_property_readonly(
      "underlying_symbol",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() && n->Snap()->underlying_pointer.node && n->Snap()->underlying_pointer.node->Snap()
          ? n->Snap()->underlying_pointer.node->Snap()->symbol
          : "";
      },
      "主力合约.")
    .def_property_readonly(
      "expire_datetime",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() ? (n->Snap()->expire_datetime / 1e9) : 0;
      },
      "最后交易时间.")
    .def_property_readonly("trading_time",
      [](std::shared_ptr<InstrumentNode> n) {
        py::dict res;
        if (n && n->Snap()) {
          auto trading_time = n->Snap()->trading_time;
          py::list day_list, night_list;
          for (auto f : trading_time.day) {
            py::list l;
            l.append(py::str(f[0]));
            l.append(py::str(f[1]));
            day_list.append(l);
          }
          for (auto f : trading_time.night) {
            py::list l;
            l.append(py::str(f[0]));
            l.append(py::str(f[1]));
            night_list.append(l);
          }
          res["day"] = day_list;
          res["night"] = night_list;
        }
        return res;
      })
    .def_property_readonly("datetime",
      [](std::shared_ptr<InstrumentNode> n) {
        return EpochNanoToHumanTime(n->Latest()->exchange_time);
      })
    .def_property_readonly("ins_class",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() ? GetInsClass(n->Snap()->product_class) : "";
      })
    .def_property_readonly("last_exercise_datetime",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() ? static_cast<double>(n->Snap()->last_exercise_day / 1e9) : TQ_NAN;
      })
    .def_property_readonly("option_class",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() && n->Snap()->option_class == md::OptionClass::kPut ? "PUT" : "CALL";
      })
    .def_property_readonly("exercise_type",
      [](std::shared_ptr<InstrumentNode> n) {
        return n && n->Snap() && n->Snap()->exercise_type == md::OptionExerciseType::kEurope ? "E" : "A";
      })
    .def("_get_underlying_symbol",
      [](std::shared_ptr<InstrumentNode> n, bool is_historical = false) {
        if (is_historical && n && n->Historical() && n->Historical()->underlying_pointer.node) {
          return n->Historical()->underlying_pointer.node->Latest()->symbol;
        } else if (!is_historical && n && n->Snap() && n->Snap()->underlying_pointer.node) {
          return n->Snap()->underlying_pointer.node->Latest()->symbol;
        }
        return md::SymbolType("");
      })
    .def("_get_datetime",
      [](std::shared_ptr<InstrumentNode> n, bool is_historical = false) {
        EpochNano nano_time = 0;
        if (is_historical && n && n->Historical()) {
          nano_time = n->Historical()->exchange_time;
        } else if (!is_historical && n && n->Snap()) {
          nano_time = n->Snap()->exchange_time;
        }
        return EpochNanoToHumanTime(nano_time);
      })
    .def("__repr__", [](std::shared_ptr<InstrumentNode> n) {
      return GetRepr(n);
    });

  py::class_<TradingStatus, std::shared_ptr<TradingStatus>>(m, "TradingStatus")
    .def_property_readonly(
      "symbol",
      [](std::shared_ptr<TradingStatus> s) {
        return s->symbol;
      },
      "合约代码")
    .def_property_readonly(
      "trade_status",
      [](std::shared_ptr<TradingStatus> s) {
        return s->status;
      },
      R"pbdoc(交易状态, 对于每个在交易所交易的品种，它在任意时刻都处于以下三种状态之一.

      * AUCTIONORDERING : 集合竞价报单, 允许用户报单, 报单不会立即成交, 而是等到集合竞价撮合阶段成交

      * CONTINOUS : 连续交易. 主要的交易时段

      * NOTRADING : 非交易时段, 例如午休时间、收盘时间、集合竞价撮合. 不允许用户报单

 )pbdoc");

  // 委托单对象
  py::class_<OrderNode, std::shared_ptr<OrderNode>>(m, "Order")
    .FIELD(OrderNode, order_id, order_id, std::string(""),
      R"pbdoc(委托单ID, 对于一个用户的所有委托单，这个ID都是不重复的, 不同柜台的委托单号规则:

        * :py:class:`~tqsdk2.TqSim` : 委托单号为自增长序列, 如 "0"、"1" 

        * :py:class:`~tqsdk2.TqKq` : 快期模拟柜台, 委托单号规则为: **当前连接 session_id + 自增长序列 + 交易单元编号**, 中间使用点号 "." 进行分割

        * :py:class:`~tqsdk2.TqAccount` : 中继实盘同快期模拟柜台 :py:class:`~tqsdk2.TqKq`

        * :py:class:`~tqsdk2.TqCtp` : 直连 CTP 柜台, 委托单号规则为: **报单引用类型 + 连接 session_id + CTP 前置编号**, 中间使用 "|" 进行分割 

        * :py:class:`~tqsdk2.TqRohon` : 融航资管柜台同直连 CTP 柜台 :py:class:`~tqsdk2.TqCtp` 
     )pbdoc")
    .FIELD(OrderNode, exchange_order_id, exchange_order_id, std::string(""), "交易所单号.")
    .FIELD(OrderNode, exchange_id, exchange_id, std::string(""), "交易所.")
    .FIELD(OrderNode, instrument_id, instrument_id, std::string(""), "委托合约代码.")
    .FIELD(OrderNode, volume_orign, volume_orign, 0, "总报单手数.")
    .FIELD(OrderNode, volume_left, volume_left, 0, "未成交手数.")
    .FIELD(OrderNode, limit_price, limit_price, TQ_NAN, "委托价格.")
    .FIELD(OrderNode, insert_date_time, insert_date_time, static_cast<md::EpochNano>(0), "下单时间.")
    .FIELD(OrderNode, last_msg, status_msg, std::string(""), "委托单状态信息.")
    .FIELD(OrderNode, investor_id, investor_id, std::string(""), "投资者帐号.")
    .FIELD(OrderNode, unit_id, unit_id, 0, "交易单元.")
    .def_property_readonly(
      "direction",
      [](std::shared_ptr<OrderNode> o) {
        return GetDirection(o->Latest()->direction);
      },
      "下单方向, BUY=买, SELL=卖.")
    .def_property_readonly(
      "offset",
      [](std::shared_ptr<OrderNode> o) {
        return GetOffSet(o->Latest()->offset);
      },
      "开平标志, OPEN=开仓, CLOSE=平仓, CLOSETODAY=平今.")
    .def_property_readonly(
      "price_type",
      [](std::shared_ptr<OrderNode> o) {
        return GetPriceType(o->Latest()->price_type);
      },
      "价格类型, ANY=市价, LIMIT=限价.")
    .def_property_readonly(
      "volume_condition",
      [](std::shared_ptr<OrderNode> o) {
        return GetVolumeCondition(o->Latest()->volume_condition);
      },
      "手数条件, ANY=任何数量, MIN=最小数量, ALL=全部数量.")
    .def_property_readonly(
      "time_condition",
      [](std::shared_ptr<OrderNode> o) {
        return GetTimeCondition(o->Latest()->time_condition);
      },
      "时间条件, IOC=立即完成，否则撤销, GFS=本节有效, GFD=当日有效, GTC=撤销前有效, GFA=集合竞价有效.")
    .def_property_readonly("status",
      [](std::shared_ptr<OrderNode> o) {
        return GetStatus(o);
      })
    .def("_get_status",
      [](std::shared_ptr<OrderNode> o, bool is_historical) {
        return GetStatus(o, is_historical);
      })
    .def_property_readonly(
      "is_dead",
      [](std::shared_ptr<OrderNode> o) {
        return o->Latest()->status == future::OrderStatus::kDead;
      },
      "委托单是否确定已死亡（以后一定不会再产生成交）(注意，False "
      "不代表委托单还存活，有可能交易所回来的信息还在路上或者丢掉了)")
    .def_property_readonly(
      "is_online",
      [](std::shared_ptr<OrderNode> o) {
        return o->Latest()->status == future::OrderStatus::kAlive && !o->Latest()->exchange_order_id.empty();
      },
      "委托单是否确定已报入交易所并等待成交 (注意，返回 False "
      "不代表确定未报入交易所，有可能交易所回来的信息还在路上或者丢掉了)")
    .def_property_readonly(
      "is_error",
      [](std::shared_ptr<OrderNode> o) {
        return o->Latest()->status == future::OrderStatus::kDead && o->Latest()->exchange_order_id.empty();
      },
      "委托单是否确定是错单（即下单失败，一定不会有成交）(注意，返回 False "
      "不代表确定不是错单，有可能交易所回来的信息还在路上或者丢掉了)")
    .def("__len__",
      [](std::shared_ptr<OrderNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<OrderNode> node) {
      return GetRepr(node);
    });

  //// 委托单对象集合
  BindMap<std::map<std::string, std::shared_ptr<OrderNode>>>(m, "Orders");

  // 成交对象
  py::class_<TradeNode, std::shared_ptr<TradeNode>>(m, "Trade")
    .FIELD(TradeNode, order_id, order_id, std::string(""), "委托单ID, 对于一个用户的所有委托单，这个ID都是不重复的.")
    .FIELD(TradeNode, trade_id, exchange_trade_id, std::string(""), "成交ID.")
    .FIELD(TradeNode, exchange_trade_id, exchange_trade_id, std::string(""), "交易所成交编号.")
    .FIELD(TradeNode, exchange_id, exchange_id, std::string(""), "交易所.")
    .FIELD(TradeNode, instrument_id, instrument_id, std::string(""), "交易所内的合约代码.")
    .FIELD(TradeNode, price, price, TQ_NAN, "成交价格.")
    .FIELD(TradeNode, volume, volume, 0, "成交手数.")
    .def_property_readonly(
      "trade_date_time",
      [](std::shared_ptr<TradeNode> t) {
        return t->Latest()->trade_date_time;
      },
      "成交时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数.")
    .def_property_readonly(
      "direction",
      [](std::shared_ptr<TradeNode> t) {
        return GetDirection(t->Latest()->direction);
      },
      "下单方向, BUY=买, SELL=卖.")
    .def_property_readonly(
      "offset",
      [](std::shared_ptr<TradeNode> t) {
        return GetOffSet(t->Latest()->offset);
      },
      "开平标志, OPEN=开仓, CLOSE=平仓, CLOSETODAY=平今.")
    .def("__len__",
      [](std::shared_ptr<TradeNode> node) {
        return 1;
      })
    .def("__getitem__",
      [](std::shared_ptr<TradeNode> node, const std::string& field) {
        // TODO 需要精简
        if (field == "order_id") {
          return node && node->Latest() ? node->Latest()->order_id : std::string();
        } else if (field == "trade_id" || field == "exchange_trade_id") {
          return node && node->Latest() ? node->Latest()->exchange_trade_id : std::string();
        } else if (field == "exchange_id") {
          return node && node->Latest() ? node->Latest()->exchange_id : std::string();
        } else if (field == "instrument_id") {
          return node && node->Latest() ? node->Latest()->instrument_id : std::string();
        } else {
          throw std::invalid_argument("field not existed.");
        }
      })
    .def("__repr__", [](std::shared_ptr<TradeNode> node) {
      return GetRepr(node);
    });

  // 成交对象集合
  BindMap<std::map<std::string, std::shared_ptr<TradeNode>>>(m, "Trades");

  // 账户对象
  py::class_<AccountNode, std::shared_ptr<AccountNode>>(m, "Account")
    .FIELD(AccountNode, currency, currency, std::string("CNY"), R"pbdoc( 币种.)pbdoc")
    .FIELD(AccountNode, pre_balance, pre_balance, TQ_NAN, "昨日账户权益(不包含期权).")
    .FIELD(AccountNode, balance, balance, TQ_NAN, "账户权益.")
    .FIELD(AccountNode, client_equity, client_equity, TQ_NAN, "客户权益.")
    .FIELD(AccountNode, available, available, TQ_NAN,
      "可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）.")
    .FIELD(AccountNode, float_profit, float_profit, TQ_NAN, "浮动盈亏.")
    .FIELD(AccountNode, position_profit, position_profit, TQ_NAN, "持仓盈亏.")
    .FIELD(AccountNode, close_profit, close_profit, TQ_NAN, "本交易日内平仓盈亏.")
    .FIELD(AccountNode, frozen_margin, frozen_margin, TQ_NAN, "冻结保证金.")
    .FIELD(AccountNode, margin, margin, TQ_NAN, "保证金占用.")
    .FIELD(AccountNode, frozen_commission, frozen_commission, TQ_NAN, "冻结手续费.")
    .FIELD(AccountNode, commission, commission, TQ_NAN, "本交易日内交纳的手续费.")
    .FIELD(AccountNode, frozen_premium, frozen_premium, TQ_NAN, "冻结权利金.")
    .FIELD(AccountNode, premium, premium, TQ_NAN, "权利金.")
    .FIELD(AccountNode, deposit, deposit, TQ_NAN, "入金金额.")
    .FIELD(AccountNode, withdraw, withdraw, TQ_NAN, "出金金额.")
    .FIELD(AccountNode, risk_ratio, risk_ratio, TQ_NAN, "风险度.")
    .FIELD(AccountNode, market_value, option_market_value, TQ_NAN, "期权市值.")
    .FIELD(AccountNode, ctp_balance, balance, TQ_NAN, "期货公司返回的balance.")
    .FIELD(AccountNode, ctp_available, available, TQ_NAN, "期货公司返回的available.")
    .FIELD(AccountNode, investor_id, investor_id, std::string(""), "投资者帐号.")
    .def("__len__",
      [](std::shared_ptr<AccountNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<AccountNode> node) {
      return GetRepr(node);
    });

  // 持仓对象 https://doc.shinnytech.com/tqsdk/latest/reference/tqsdk.objs.html
  py::class_<PositionNode, std::shared_ptr<PositionNode>>(m, "Position")
    .FIELD(PositionNode, exchange_id, exchange_id, std::string(""), "交易所.")
    .FIELD(PositionNode, instrument_id, instrument_id, std::string(""), "合约代码.")
    .FIELD(PositionNode, pos_long_his, subpos_long_spec.volume_his, 0, "多头老仓手数.")
    .FIELD(PositionNode, pos_long_today, subpos_long_spec.volume_today, 0, "多头今仓手数.")
    .FIELD(PositionNode, pos_short_his, subpos_short_spec.volume_his, 0, "空头老仓手数.")
    .FIELD(PositionNode, pos_short_today, subpos_short_spec.volume_today, 0, "空头今仓手数.")
    .FIELD(PositionNode, volume_long_today, subpos_long_spec.volume_today, 0, "多头今仓手数.")
    .FIELD(PositionNode, volume_long_his, subpos_long_spec.volume_his, 0, "多头老仓手数.")
    .FIELD(PositionNode, volume_long, volume_long(), 0, "多头手数.")
    .FIELD(PositionNode, volume_long_frozen_today, subpos_long_spec.volume_today_frozen, 0, "多头今仓冻结.")
    .FIELD(PositionNode, volume_long_frozen_his, subpos_long_spec.volume_his_frozen, 0, "多头老仓冻结.")
    .FIELD(PositionNode, volume_short_today, subpos_short_spec.volume_today, 0, "空头今仓手数.")
    .FIELD(PositionNode, volume_short_his, subpos_short_spec.volume_his, 0, "空头今仓手数.")
    .FIELD(PositionNode, volume_short, volume_short(), 0, "空头手数.")
    .FIELD(PositionNode, volume_short_frozen_today, subpos_short_spec.volume_today_frozen, 0, "空头今仓冻结.")
    .FIELD(PositionNode, volume_short_frozen_his, subpos_short_spec.volume_his_frozen, 0, "空头老仓冻结.")
    .FIELD(PositionNode, open_price_long, subpos_long_spec.open_price, TQ_NAN, "多头开仓均价.")
    .FIELD(PositionNode, open_price_short, subpos_short_spec.open_price, TQ_NAN, "空头开仓均价.")
    .FIELD(PositionNode, open_cost_long, subpos_long_spec._open_cost, TQ_NAN, "多头开仓成本.")
    .FIELD(PositionNode, open_cost_short, subpos_short_spec._open_cost, TQ_NAN, "空头开仓成本.")
    .FIELD(PositionNode, position_price_long, subpos_long_spec.position_price, TQ_NAN, "多头持仓均价.")
    .FIELD(PositionNode, position_price_short, subpos_short_spec.position_price, TQ_NAN, "空头持仓均价.")
    .FIELD(PositionNode, position_cost_long, subpos_long_spec._position_cost, TQ_NAN, "多头持仓成本.")
    .FIELD(PositionNode, position_cost_short, subpos_short_spec._position_cost, TQ_NAN, "空头持仓成本.")
    .FIELD(PositionNode, float_profit_long, subpos_long_spec.float_profit, TQ_NAN, "多头浮动盈亏.")
    .FIELD(PositionNode, float_profit_short, subpos_short_spec.float_profit, TQ_NAN, "空头浮动盈亏.")
    .FIELD(PositionNode, float_profit, float_profit(), TQ_NAN, "浮动盈亏.")
    .FIELD(PositionNode, position_profit_long, subpos_long_spec.position_profit, TQ_NAN, "多头持仓盈亏.")
    .FIELD(PositionNode, position_profit_short, subpos_short_spec.position_profit, TQ_NAN, "空头持仓盈亏.")
    .FIELD(PositionNode, position_profit, position_profit(), TQ_NAN,
      "持仓盈亏 （持仓盈亏: 相对于上一交易日结算价的盈亏），期权持仓盈亏为 0.")
    .FIELD(PositionNode, margin_long, subpos_long_spec.margin, TQ_NAN, "多头占用保证金.")
    .FIELD(PositionNode, margin_short, subpos_short_spec.margin, TQ_NAN, "空头占用保证金.")
    .FIELD(PositionNode, margin, margin(), TQ_NAN, "占用保证金.")
    .FIELD(PositionNode, market_value_long, subpos_long_spec.market_value, TQ_NAN, "期权权利方市值.")
    .FIELD(PositionNode, market_value_short, subpos_short_spec.market_value, TQ_NAN, "期权义务方市值.")
    .FIELD(PositionNode, pos, volume_net(), 0, "净持仓手数.")
    .FIELD(PositionNode, pos_long, volume_long(), 0, "多头手数.")
    .FIELD(PositionNode, pos_short, volume_short(), 0, "空头手数.")
    .FIELD(PositionNode, investor_id, investor_id, std::string(""), "投资者帐号.")
    .FIELD(PositionNode, close_profit, close_profit(), TQ_NAN, "平仓盈亏.")
    .FIELD(PositionNode, volume_long_yd, subpos_long_spec.volume_yesterday, 0, "昨多仓手数.")
    .FIELD(PositionNode, volume_short_yd, subpos_short_spec.volume_yesterday, 0, "昨多仓手数.")
    .FIELD(PositionNode, unit_id, unit_id, 0, "交易单元.")
    .FIELD(PositionNode, symbol, symbol(), std::string(""), "合约代码.")
    .def("__len__",
      [](std::shared_ptr<PositionNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<PositionNode> node) {
      return GetRepr(node);
    });

  //// 持仓对象集合
  BindMap<std::map<std::string, std::shared_ptr<PositionNode>>>(m, "Positions");

  /*
   * 股票业务声明接口
   */
  py::class_<security::AccountNode, std::shared_ptr<security::AccountNode>>(m, "SecurityAccount")
    .FIELD(security::AccountNode, user_id, user_id, std::string(), "资金账号.")
    .FIELD(security::AccountNode, currency, currency, std::string("CNY"), "币种")
    .FIELD(security::AccountNode, available, available, 0.0, "可用金额")
    .FIELD(security::AccountNode, available_his, available_his, 0.0, "期初可用")
    .FIELD(security::AccountNode, buy_frozen_balance, buy_frozen_balance, 0.0, "委托买入冻结金额")
    .FIELD(security::AccountNode, buy_frozen_fee, buy_frozen_fee, 0.0, "委托买入冻结费用")
    .FIELD(security::AccountNode, buy_balance_today, buy_balance_today, 0.0, "当日买入占用资金")
    .FIELD(security::AccountNode, buy_fee_today, buy_fee_today, 0.0, "当日买入费用")
    .FIELD(security::AccountNode, sell_balance_today, sell_balance_today, 0.0, "当日卖出释放资金")
    .FIELD(security::AccountNode, sell_fee_today, sell_fee_today, 0.0, "当日卖出交易费用金额")
    .FIELD(security::AccountNode, deposit, deposit, 0.0, "当日入今")
    .FIELD(security::AccountNode, withdraw, withdraw, 0.0, "当日出金")
    .FIELD(security::AccountNode, drawable, drawable, 0.0, "可取资金")
    .FIELD(security::AccountNode, market_value, market_value, 0.0, "持仓市值")
    .FIELD(security::AccountNode, asset, asset, 0.0, "总资产")
    .FIELD(security::AccountNode, asset_his, asset_his, 0.0, "期初资产")
    .FIELD(security::AccountNode, dividend_balance_today, dividend_balance_today, 0.0, "当日分红金额")
    .FIELD(security::AccountNode, cost, cost, 0.0, "当前买入成本")
    .FIELD(security::AccountNode, hold_profit, hold_profit, 0.0, "持仓盈亏")
    .FIELD(security::AccountNode, float_profit_today, float_profit_today, 0.0, "当日浮动盈亏")
    .FIELD(security::AccountNode, real_profit_today, real_profit_today, 0.0, "当日实现盈亏")
    .FIELD(security::AccountNode, profit_today, profit_today, 0.0, "当日盈亏")
    .FIELD(security::AccountNode, profit_rate_today, profit_rate_today, 0.0, "当日收益率")
    .def("__len__",
      [](std::shared_ptr<security::AccountNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<security::AccountNode> node) {
      FieldSerializer s;
      s.FromVar(node->Latest());
      std::string json;
      s.ToString(&json);
      return json;
    });

  py::class_<security::PositionNode, std::shared_ptr<security::PositionNode>>(m, "SecurityPosition")
    .FIELD(security::PositionNode, user_id, user_id, std::string(), "资金账号.")
    .FIELD(security::PositionNode, exchange_id, exchange_id, std::string(), "交易所代码")
    .FIELD(security::PositionNode, instrument_id, instrument_id, std::string(), "证券代码")
    .FIELD(security::PositionNode, symbol, symbol(), std::string(), "证券代码")
    .FIELD(security::PositionNode, create_date, create_date, std::string(), "建仓日期")
    .FIELD(security::PositionNode, volume_his, volume_his, 0, "期初持仓数量")
    .FIELD(security::PositionNode, volume, volume, 0, "当前数量")
    .FIELD(security::PositionNode, last_price, last_price, TQ_NAN, "最新价")
    .FIELD(security::PositionNode, buy_volume_today, buy_volume_today, 0, "今买数量")
    .FIELD(security::PositionNode, buy_balance_today, buy_balance_today, TQ_NAN, "今买金额")
    .FIELD(security::PositionNode, buy_fee_today, buy_fee_today, TQ_NAN, "今买费用")
    .FIELD(security::PositionNode, sell_volume_today, sell_volume_today, 0, "今卖数量")
    .FIELD(security::PositionNode, sell_balance_today, sell_balance_today, TQ_NAN, "今卖金额")
    .FIELD(security::PositionNode, sell_fee_today, sell_fee_today, TQ_NAN, "今卖费用")
    .FIELD(security::PositionNode, shared_volume_today, shared_volume_today, 0, "今送股数量")
    .FIELD(security::PositionNode, devidend_balance_today, devidend_balance_today, TQ_NAN, "今红利金额")
    .FIELD(security::PositionNode, buy_volume_his, buy_volume_his, 0, "前买数量")
    .FIELD(security::PositionNode, buy_balance_his, buy_balance_his, TQ_NAN, "前买金额")
    .FIELD(security::PositionNode, buy_fee_his, buy_fee_his, TQ_NAN, "前买费用")
    .FIELD(security::PositionNode, sell_volume_his, sell_volume_his, 0, "前卖数量")
    .FIELD(security::PositionNode, sell_balance_his, sell_balance_his, TQ_NAN, "前卖金额")
    .FIELD(security::PositionNode, sell_fee_his, sell_fee_his, TQ_NAN, "前卖费用")
    .FIELD(security::PositionNode, cost_his, cost_his, TQ_NAN, "前买入成本")
    .FIELD(security::PositionNode, cost, cost, TQ_NAN, "当前成本")
    .FIELD(security::PositionNode, market_value_his, market_value_his, TQ_NAN, "期初市值")
    .FIELD(security::PositionNode, market_value, market_value, TQ_NAN, "持仓市值")
    .FIELD(security::PositionNode, float_profit_today, float_profit_today, TQ_NAN, "当日浮动盈亏")
    .FIELD(security::PositionNode, real_profit_today, real_profit_today, TQ_NAN, "当日实现盈亏")
    .FIELD(security::PositionNode, profit_today, profit_today, TQ_NAN, "当日盈亏")
    .FIELD(security::PositionNode, profit_rate_today, profit_rate_today, TQ_NAN, "当日收益率")
    .FIELD(security::PositionNode, hold_profit, hold_profit, TQ_NAN, "持仓盈亏")
    .FIELD(security::PositionNode, real_profit_total, real_profit_total, TQ_NAN, "累计实现盈亏")
    .FIELD(security::PositionNode, real_profit_total_his, real_profit_total_his, TQ_NAN, "期初累计实现盈亏")
    .FIELD(security::PositionNode, profit_total, profit_total, TQ_NAN, "总盈亏")
    .FIELD(security::PositionNode, profit_rate_total, profit_rate_total, TQ_NAN, "累计收益率")
    .def("__len__",
      [](std::shared_ptr<security::PositionNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<security::PositionNode> node) {
      FieldSerializer s;
      s.FromVar(node->Latest());
      std::string json;
      s.ToString(&json);
      return json;
    });

  py::class_<security::OrderNode, std::shared_ptr<security::OrderNode>>(m, "SecuritiesOrder")
    .FIELD(security::OrderNode, user_id, user_id, std::string(), "资金账户")
    .FIELD(security::OrderNode, exchange_id, exchange_id, std::string(), "交易所")
    .FIELD(security::OrderNode, instrument_id, instrument_id, std::string(), "证券代码")
    .FIELD(security::OrderNode, order_id, order_id, std::string(), "委托单号")
    .FIELD(security::OrderNode, volume_orign, volume_orign, 0, "委托手数.")
    .FIELD(security::OrderNode, volume_left, volume_left, 0, "未成交手数.")
    .FIELD(security::OrderNode, limit_price, limit_price, TQ_NAN, "委托价格.")
    .FIELD(security::OrderNode, insert_date_time, insert_date_time, static_cast<md::EpochNano>(0), "下单时间.")
    .FIELD(security::OrderNode, status_msg, status_msg, std::string(), "委托单状态信息.")
    .def_property_readonly(
      "direction",
      [](std::shared_ptr<security::OrderNode> o) {
        return o->Latest()->direction == security::Direction::kBuy ? "BUY" : "SELL";
      },
      "下单方向, BUY=买, SELL=卖.")
    .def_property_readonly(
      "price_type",
      [](std::shared_ptr<security::OrderNode> o) {
        return o->Latest()->price_type == security::PriceType::kAny ? "ANY" : "LIMIT";
      },
      "价格类型, ANY=市价, LIMIT=限价.")
    .def_property_readonly("status",
      [](std::shared_ptr<security::OrderNode> o) {
        switch (o->Latest()->status) {
          case security::OrderStatus::kAlive: return "ALIVE";
          case security::OrderStatus::kDead: return "FINISHED";
          default: return "Unknown ORDER_STATUS_TYPE";
        }
      })
    .def("_get_status",
      [](std::shared_ptr<security::OrderNode> o, bool is_historical) {
        if (is_historical && o->Historical() == nullptr)
          return "ALIVE";

        auto content = is_historical && o->Historical() ? o->Historical() : o->Latest();
        switch (content->status) {
          case security::OrderStatus::kAlive: return "ALIVE";
          case security::OrderStatus::kDead: return "FINISHED";
          default: return "Unknown ORDER_STATUS_TYPE";
        }
      })
    .def("__len__",
      [](std::shared_ptr<security::OrderNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<security::OrderNode> node) {
      FieldSerializer s;
      s.FromVar(node->Latest());
      std::string json;
      s.ToString(&json);
      return json;
    });

  py::class_<security::TradeNode, std::shared_ptr<security::TradeNode>>(m, "SecuritiesTrade")
    .FIELD(security::TradeNode, user_id, user_id, std::string(), "资金账户")
    .FIELD(security::TradeNode, trade_id, exchange_trade_id, std::string(), "成交合同编号")
    .FIELD(security::TradeNode, exchange_id, exchange_id, std::string(), "交易所")
    .FIELD(security::TradeNode, instrument_id, instrument_id, std::string(), "证券代码")
    .FIELD(security::TradeNode, order_id, order_id, std::string(), "委托单号, 对应委托单的 order_id")
    .FIELD(security::TradeNode, exchange_trade_id, exchange_trade_id, std::string(), "交易所成交编号")
    .FIELD(security::TradeNode, price, price, TQ_NAN, "成交价格")
    .FIELD(security::TradeNode, volume, volume, 0, "成交手数")
    .FIELD(security::TradeNode, balance, balance(), 0.0, "成交发生金额")
    .FIELD(security::TradeNode, fee, fee, 0.0, "成交手续费")
    .def_property_readonly(
      "direction",
      [](std::shared_ptr<security::TradeNode> t) {
        return t->Latest()->direction == security::Direction::kBuy ? "BUY" : "SELL";
      },
      "下单方向, BUY=买, SELL=卖.")
    .def_property_readonly(
      "trade_date_time",
      [](std::shared_ptr<security::TradeNode> t) {
        return t->Latest()->trade_date_time;
      },
      "成交时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数.")
    .def("__len__",
      [](std::shared_ptr<security::TradeNode> node) {
        return 1;
      })
    .def("__repr__", [](std::shared_ptr<security::TradeNode> node) {
      FieldSerializer s;
      s.FromVar(node->Latest());
      std::string json;
      s.ToString(&json);
      return json;
    });

  /**
   * TqAuth 信易账户类
   */
  py::class_<TqAuth>(m, "TqAuth")
    .def(py::init<const std::string&, const std::string&>(), py::arg("user_name"), py::arg("password"), R"pbdoc( 

      用户认证类, 使用信易账户进行认证授权, 信易账户可以通过 https://account.shinnytech.com/ 进行注册、登录和管理.

      Args:
        user_name (str): [必填] 信易账户，可以是 邮箱、用户名、手机号.

        password (str):  [必填] 信易账户密码.

      Returns:
        返回当前认证实例

      Example::

          # 登录快期模拟
          from tqsdk2 import TqApi, TqAuth, TqAccount
          api = TqApi(TqKq(), auth=TqAuth("信易账户", "账户密码"))
          api.close()

     )pbdoc");

  /**
   * 天勤2 账户类
   */
  py::class_<TqUser> account(m, "TqUser");

  py::class_<TqAccount>(m, "TqAccount", account)
    .def(py::init<const std::string&, const std::string&, const std::string&, int, const std::string&>(),
      py::arg("broker_id"), py::arg("account_id"), py::arg("password"),
      py::arg("default_trading_unit") = ktrade_unit_unset, py::arg("_td_url") = std::string(),
      R"pbdoc(
      天勤2实盘类,  通过中继服务器接入券商柜台.

      Args:
        broker_id (str):            [必填] 期货公司, 支持的期货公司列表见 https://www.shinnytech.com/blog/tq-support-broker/.

        account_id (str):           [必填] 帐号.

        password (str):             [必填] 密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.

     )pbdoc");

  py::class_<TqKq>(m, "TqKq", account)
    .def(py::init<int, const std::string&>(), py::arg("default_trading_unit") = ktrade_unit_unset,
      py::arg("_td_url") = std::string(), R"pbdoc( 
      天勤2 快期模拟交易类, 快期模拟账户与信易账户相匹配, 该账户的信息在快期PC、快期App、天勤和天勤2不同产品之间也是同步的.

      Args:
        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
    )pbdoc");

  py::class_<TqKqStock>(m, "TqKqStock", account)
    .def(py::init<int, const std::string&>(), py::arg("default_trading_unit") = ktrade_unit_unset,
      py::arg("_td_url") = std::string(), R"pbdoc( 
      天勤2 快期股票模拟交易类, 快期模拟账户与信易账户相匹配

      Args:
        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
    )pbdoc");

  py::class_<TqSim> tq_sim(m, "TqSim", account);
  tq_sim.def(py::init<double, const std::string&>(), py::arg("init_balance") = 10000000.0,
    py::arg("account_id") = std::string(), R"pbdoc( 
      天勤2模拟交易类.

        该类实现了一个本地的模拟账户，并且在内部完成撮合交易，在回测模式下，只能使用 TqSim 账户来交易。

      Args:
        init_balance (float): [可选]初始资金, 默认为 1000 万

        account_id (str):     [可选]帐号, 默认为 TQSIM

     )pbdoc");
  tq_sim.def("set_margin", &TqSim::SetMargin, py::arg("symbol"), py::arg("margin"), R"pbdoc( 
      设置指定合约模拟交易的每手保证金。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

        margin (float): 每手保证金

      Returns:
        float: 设置的每手保证金

      Example::

          from tqsdk2 import TqApi, TqAuth, TqSim
          sim = TqSim()
          api = TqApi(sim, auth=TqAuth("信易账户", "账户密码"))
          sim.set_margin("SHFE.cu2201", 26000)
          print(sim.get_margin("SHFE.cu2201"))
          api.close()

     )pbdoc");
  tq_sim.def("get_margin", &TqSim::GetMargin, py::arg("symbol"), R"pbdoc( 
      获取指定合约模拟交易的每手保证金。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

      Returns:
        float: 返回合约模拟交易的每手保证金

     )pbdoc");
  tq_sim.def("set_commission", &TqSim::SetCommission, py::arg("symbol"), py::arg("commission"), R"pbdoc( 
      设置指定合约模拟交易的每手手续费。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

        commission (float): 每手手续费

      Returns:
        float: 设置的每手手续费

      Example::

          from tqsdk2 import TqApi, TqAuth, TqSim
          sim = TqSim()
          api = TqApi(sim, auth=TqAuth("信易账户", "账户密码"))
          sim.set_commission("SHFE.cu2201", 50)
          print(sim.get_commission("SHFE.cu2201"))
          api.close()

     )pbdoc");
  tq_sim.def("get_commission", &TqSim::GetCommission, py::arg("symbol"), R"pbdoc( 
      获取指定合约模拟交易的每手手续费。

      Args:
        symbol (str): 合约代码 (只支持期货合约)

      Returns:
        float: 返回合约模拟交易的每手手续费

     )pbdoc");

  py::class_<TqCtp>(m, "TqCtp", account)
    .def(py::init<const std::string&, const std::string&, const std::string&, const std::string&, const std::string&,
           const std::string&, int>(),
      py::arg("td_url") = std::string(), py::arg("broker_id") = std::string(), py::arg("app_id") = std::string(),
      py::arg("auth_code") = std::string(), py::arg("user_name") = std::string(), py::arg("password") = std::string(),
      py::arg("default_trading_unit") = ktrade_unit_unset, R"pbdoc( 
      天勤2 实盘(直连CTP)账户类.

        创建天勤实盘(直连CTP)实例。

      Args:
        td_url (str):               [必填]CTP柜台地址.

        broker_id (str):            [必填]CTP交易前置的Broker ID, eg: 2020.

        app_id (str):               [必填]期货公司授权ID.

        auth_code (str):            [必填]期货公司授权码.

        user_name (str):            [必填]帐号.

        password (str):             [必填]密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.
     )pbdoc");

  py::class_<TqRohon>(m, "TqRohon", account)
    .def(py::init<const std::string&, const std::string&, const std::string&, const std::string&, const std::string&,
           const std::string&, int>(),
      py::arg("td_url") = std::string(), py::arg("broker_id") = std::string(), py::arg("app_id") = std::string(),
      py::arg("auth_code") = std::string(), py::arg("user_name") = std::string(), py::arg("password") = std::string(),
      py::arg("default_trading_unit") = ktrade_unit_unset, R"pbdoc( 
      天勤2 融航资管账户类.

        创建融航资管账户实例。

      Args:
        td_url (str):               [必填]CTP柜台地址.

        broker_id (str):            [必填]CTP交易前置的Broker ID, eg: 2020.

        app_id (str):               [必填]期货公司授权ID.

        auth_code (str):            [必填]期货公司授权码.

        user_name (str):            [必填]帐号.

        password (str):             [必填]密码.

        default_trading_unit (int): [可选] 默认交易单元, 如果指定该参数, 后续下单查询等操作均视为对该交易单元的操作.

      Example::

          # 登录融航资管
          from tqsdk2 import TqApi, TqAuth, TqRohon
          account = TqRohon(td_url="tcp://129.211.138.170:10001", broker_id="RohonDemo", app_id="融航模拟的appid", auth_code= "融航模拟authcode", user_name="融航模拟账户", password="融航模拟账户密码")
          api = TqApi(account = account, auth= TqAuth("信易账户","账户密码"))

     )pbdoc");

  py::class_<TargetPosTask>(m, "TargetPosTask")
    .def(py::init<TqPythonApi&, const std::string&, const py::object&, const std::string&, int>(), py::arg("api"),
      py::arg("symbol"), py::arg("price") = "ACTIVE", py::arg("offset_priority") = "今昨,开",
      py::arg("trading_unit") = ktrade_unit_unset, R"pbdoc( 
      天勤2 目标持仓 task, 该 task 可以将指定合约调整到目标头寸.
      创建目标持仓task实例，负责调整归属于该task的持仓 (默认为整个账户的该合约净持仓).
      
      Args:
      api (TqApi):      TqApi实例，该task依托于指定api下单/撤单
      symbol (str):     负责调整的合约代码
      price (str):      [可选]下单方式, 默认为 "ACTIVE"。
        "ACTIVE"：对价下单，在持仓调整过程中，若下单方向为买，对价为卖一价；若下单方向为卖，对价为买一价。
        "PASSIVE"：对价下单，在持仓调整过程中，若下单方向为买，对价为买一价；若下单方向为卖，对价为卖一价。
      offset_priority (str): [可选]开平仓顺序，昨=平昨仓，今=平今仓，开=开仓，逗号=等待之前操作完成
      trading_unit(int): [可选] 交易单元编号

      Example::

        from tqsdk2 import TqApi, TqAuth, TargetPosTask

        api = TqApi(auth=TqAuth("信易账户","账户密码"))
        quote = api.get_quote("SHFE.cu2201")

        def get_price(direction):
            # 在 BUY 时使用买一价加一档价格，SELL 时使用卖一价减一档价格
            if direction == "BUY":
                price = quote.bid_price1 + quote.price_tick
            else:
                price = quote.ask_price1 - quote.price_tick
            # 如果 price 价格是 nan，使用最新价报单
            if price != price:
                price = quote.last_price
            return price

        target_pos = TargetPosTask(api = api, symbol = "SHFE.cu2201", price=get_price)

        while True:
            api.wait_update()
            target_pos.set_target_volume(5)

        api.close()
        
     )pbdoc")
    .def("set_target_volume", &TargetPosTask::SetTargetVolume, R"pbdoc( 
      设置目标持仓手数.
      创建天勤实盘实例。
      
      Args:
      volume (int): 目标持仓手数，正数表示多头，负数表示空头，0表示空仓 )pbdoc");

  py::class_<Ta>(m, "ta").def(py::init<>());

  py::class_<Datetime>(m, "tqdatetime").def(py::init<>());

  py::class_<TaFunc>(m, "tafunc").def(py::init<>());

  py::class_<TqPythonApi>(m, "TqApi")
    .def(py::init<py::object&, py::object&, py::object&, py::object&, py::object&, bool, const std::string&, int,
           int64_t>(),
      py::arg("account") = TqSim(10000000.00, "TQSIM"), py::arg("auth") = nullptr, py::arg("backtest") = nullptr,
      py::arg("web_gui") = false, py::arg("debug") = false, py::arg("disable_print") = false,
      py::arg("_md_url") = std::string(), py::arg("_srandom") = 0, py::arg("_mock_date_time") = 0, R"pbdoc( 

      创建天勤2 接口实例.

      Args:
        account (None/TqSim/TqKq/TqKqStock/TqAccount/TqCtp/TqRohon): [可选] 交易账号:
          * None: 账号将根据环境变量决定, 默认为 :py:class: `~tqsdk2.TqSim` 

          * :py:class:`~tqsdk2.TqSim` : 使用 TqApi 自带的本地模拟账号 

          * :py:class:`~tqsdk2.TqKq` : 使用快期账号登录，直连行情和快期模拟交易服务器, 需提供 auth 参数

          * :py:class:`~tqsdk2.TqKqStock` : 使用快期账号登录，直连行情和快期股票模拟交易服务器, 需提供 auth 参数

          * :py:class:`~tqsdk2.TqAccount` : 使用实盘账号, 直连行情和交易中继服务器, 需提供期货公司/帐号/密码 

          * :py:class:`~tqsdk2.TqCtp` : 使用实盘账号, 直连行情和期货公司 CTP 交易服务器, 需提供期货公司/帐号/密码 

          * :py:class:`~tqsdk2.TqRohon` : 直连融航资管柜台 

        auth (TqAuth/str): [必填] 用户信易账户

          * :py:class:`~tqsdk2.TqAuth` : 信易账户类，例如：TqAuth("tianqin@qq.com", "123456"), 您可以通过 `https://account.shinnytech.com` 进行注册管理

        debug(bool/str): [可选] 是否将调试信息输出到指定文件，默认值为 False


        disable_print(bool): [可选] 是否禁用调试信息输出，默认值为 False


        backtest(TqBacktest): [可选] 进入时光机，此时强制要求 account 类型为 :py:class:`~tqsdk2.sim.TqSim`
          * :py:class:`~tqsdk2.backtest.TqBacktest` : 传入 TqBacktest 对象，进入回测模式, 在回测模式下, 由 TqBacktest 内部完成回测时间段内的行情推进和 K 线、Tick 更新.

        web_gui(bool/str): [可选]是否启用图形化界面功能, 默认不启用.
          * 启用图形化界面传入参数 web_gui=True 会每次以随机端口生成网页，也可以直接设置本机IP和端口 web_gui=[ip]:port 为网页地址，ip 可选，默认为 0.0.0.0，参考example 6

          * 为了图形化界面能够接收到程序传输的数据并且刷新，在程序中，需要循环调用 api.wait_update的形式去更新和获取数据

          * 推荐打开图形化界面的浏览器为Google Chrome 或 Firefox

      Returns:
          TqApi: 返回当前TqApi的一个副本

      Example1::

          # 使用实盘帐号直连行情和交易服务器
          from tqsdk2 import TqApi, TqAuth, TqAccount
          api = TqApi(TqAccount("H海通期货", "022631", "123456"), auth=TqAuth("信易账户", "账户密码"))

      )pbdoc")
    .def("close", &TqPythonApi::CleanUp, R"pbdoc( 
      关闭天勤接口实例并释放相应资源.
      )pbdoc")
    .def("insert_order", &TqPythonApi::InsertOrder, py::arg("symbol") = std::string(),
      py::arg("direction") = std::string(), py::arg("offset") = std::string(), py::arg("volume") = 0,
      py::arg("limit_price") = nullptr, py::arg("trading_unit") = ktrade_unit_unset, R"pbdoc(
      发送下单指令, 注意: 与 TqSdk 不同, TqSdk2 下单指令会立即发出, 无需等待用户调用 wait_update() 函数
 
      Args:
        symbol (str): 拟下单的合约symbol, 格式为 交易所代码.合约代码, 例如 "SHFE.cu1801"

        direction (str): "BUY" 或 "SELL"

        offset (str): "OPEN", "CLOSE" 或 "CLOSETODAY" (上期所和原油分平今/平昨, 平今用"CLOSETODAY", 平昨用"CLOSE"; 其他交易所直接用"CLOSE" 按照交易所的规则平仓)

        volume (int): 下单交易数量, 期货为下单手数

        trading_unit(int): [可选] 交易单元编号

      )pbdoc")
    .def("_insert_stock_order", &TqPythonApi::InsertStockOrder, py::arg("symbol") = std::string(),
      py::arg("direction") = std::string(), py::arg("volume") = 0, py::arg("limit_price") = nullptr, R"pbdoc(
      股票委托下单
 
      Args:
        symbol (str): 拟下单的证券代码 symbol, 格式为 交易所代码.合约代码, 例如 "SSE.600000"

        direction (str): "BUY" 或 "SELL"

        volume (int): 委托下单股数

      )pbdoc")
    .def("cancel_order", &TqPythonApi::CancelOrder, py::arg("order_or_order_id") = nullptr, R"pbdoc(
      发送撤单指令, 注意: 与 TqSdk 不同, TqSdk2 下单指令会立即发出, 无需等待用户调用 wait_update() 函数

      Args:
        order_or_order_id (str): 拟撤委托单或单号

      )pbdoc")
    .def("_cancel_stock_order", &TqPythonApi::CancelStockOrder, py::arg("order_or_order_id") = nullptr)
    .def("get_quote", &TqPythonApi::SubscribeQuote, py::arg("symbol"), R"pbdoc(
      获取指定合约的盘口行情

      Args:
        symbol (str): 指定合约代码, 合约代码格式为 交易所代码.合约代码. 可用的交易所代码如下：
          * CFFEX:  中金所

          * SHFE:   上期所

          * DCE:    大商所

          * CZCE:   郑商所

          * INE:    能源交易所(原油)

          * SSE:    上交所

          * SZSE:   深交所

      Returns:
        :py:class:`~tqsdk2.Quote`: 返回一个盘口行情引用, 其内容将在 wait_update() 时更新, 注意: 在 tqsdk 还没有收到行情数据包时, 此对象中各项内容为 NaN 或 0

      )pbdoc")
    .def("get_account", &TqPythonApi::GetAccount, py::arg("trading_unit") = ktrade_unit_unset, R"pbdoc( 
      获取用户账户资金信息

      Args:
          trading_unit (int): [可选] 交易单元编号

      Returns:
          :py:class:`~tqsdk2.Account`: 返回一个账户对象引用. 其内容将在 wait_update() 时更新

     )pbdoc")
    .def("get_order", py::overload_cast<const std::string&, int>(&TqPythonApi::GetOrder), py::arg("order_id"),
      py::arg("trading_unit") = ktrade_unit_unset, py::return_value_policy::reference_internal, R"pbdoc( 
      获取用户委托单信息

      Args:
        order_id (str):     [可选] 委托单号, 不填单号则返回所有委托单

        trading_unit (int): [可选] 交易单元编号

      Returns:
          :py:class:`~tqsdk2.Order`: 
            * 当指定了order_id时, 返回一个委托单对象引用. 其内容将在 wait_update() 时更新.

            * 不填 order_id 参数调用本函数, 将返回包含用户所有委托单的一个集合对象的引用, 使用方法与 dict 一致, 其中每个元素的 key 为委托单号, value 为 :py:class:`~tqsdk2.Order`

     )pbdoc")
    .def("get_order", py::overload_cast<int>(&TqPythonApi::GetOrders), py::arg("trading_unit") = ktrade_unit_unset,
      py::return_value_policy::reference_internal)
    .def("get_trade", py::overload_cast<const std::string&, int>(&TqPythonApi::GetTrade), py::arg("trade_id"),
      py::arg("trading_unit") = ktrade_unit_unset, py::return_value_policy::reference_internal, R"pbdoc( 
      获取用户成交信息

      Args:
        trade_id (str):     [可选] 成交合同编号, 不填成交号则返回所有委托单

        trading_unit (int): [可选] 交易单元编号

      Returns:
          :py:class:`~tqsdk2.Trade`: 
            * 当指定了 trade_id 时, 返回一个成交对象引用. 其内容将在 wait_update() 时更新.

            * 不填 trade_id 参数调用本函数, 将返回包含用户当前交易日所有成交记录的集合对象的引用, 使用方法与 dict 一致, 其中每个元素的 key 为成交号, value 为 :py:class:`~tqsdk2.Trade`

     )pbdoc")
    .def("get_trade", py::overload_cast<int>(&TqPythonApi::GetTrades), py::arg("trading_unit") = ktrade_unit_unset,
      py::return_value_policy::reference_internal)
    .def("get_position", py::overload_cast<const std::string&, int>(&TqPythonApi::GetPosition), py::arg("symbol"),
      py::arg("trading_unit") = ktrade_unit_unset, py::return_value_policy::reference_internal, R"pbdoc( 
      获取用户持仓信息

      Args:
        symbol (str): [可选]合约代码, 不填则返回所有持仓

        trading_unit (int): [可选] 交易单元编号

      Returns:
          :py:class:`~tqsdk2.Position`: 当指定了 symbol 时, 返回一个持仓对象引用. 其内容将在 wait_update() 时更新
          不填 symbol 参数调用本函数, 将返回包含用户所有持仓的一个集合对象的引用, 使用方法与 dict 一致, 其中每个元素的 key 为合约代码, value 为 Position

     )pbdoc")
    .def("get_position", py::overload_cast<int>(&TqPythonApi::GetPositions), "trading_unit"_a = ktrade_unit_unset,
      py::return_value_policy::reference_internal)

    .def("wait_update", &TqPythonApi::RunOnce, py::arg("deadline") = 0.0, R"pbdoc( 
      等待业务数据更新.

      调用此函数将阻塞当前线程, 等待天勤主进程发送业务数据更新并返回

      注: 它是 TqApi 中最重要的一个函数, 每次调用它时都会发生这些事:
        刷新最新的账户状态信息, 包括账户下订阅的行情、tick 和 Klines 数据.

        若启动了调仓工具模块, 则执行一次调仓条件判断和下单.

      Args:
          deadline (float): [可选]指定截止时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的秒数(time.time()), 默认没有超时(无限等待).

     )pbdoc")
    .def("_get_stock_account", &TqPythonApi::GetStockAccount, py::return_value_policy::reference_internal)
    .def("_get_stock_order", py::overload_cast<const std::string&>(&TqPythonApi::GetStockOrder), py::arg("order_id"),
      py::return_value_policy::reference_internal)
    .def("_get_stock_order", py::overload_cast<>(&TqPythonApi::GetStockOrders),
      py::return_value_policy::reference_internal)
    .def("_get_stock_trade", py::overload_cast<const std::string&>(&TqPythonApi::GetStockTrade), py::arg("trade_id"),
      py::return_value_policy::reference_internal)
    .def("_get_stock_trade", py::overload_cast<>(&TqPythonApi::GetStockTrades),
      py::return_value_policy::reference_internal)
    .def("_get_stock_position", py::overload_cast<const std::string&>(&TqPythonApi::GetStockPosition),
      py::arg("symbol"), py::return_value_policy::reference_internal)
    .def("_get_stock_position", py::overload_cast<>(&TqPythonApi::GetStockPositions),
      py::return_value_policy::reference_internal)
    .def("wait_update", &TqPythonApi::RunOnce, py::arg("deadline") = 0.0, R"pbdoc( 
      等待业务数据更新.

      调用此函数将阻塞当前线程, 等待天勤主进程发送业务数据更新并返回

      注: 它是 TqApi 中最重要的一个函数, 每次调用它时都会发生这些事:
        刷新最新的账户状态信息, 包括账户下订阅的行情、tick 和 Klines 数据.

        若启动了调仓工具模块, 则执行一次调仓条件判断和下单.

      Args:
          deadline (float): [可选]指定截止时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的秒数(time.time()), 默认没有超时(无限等待).

     )pbdoc")
    .def("is_changing", py::overload_cast<py::object, py::str>(&TqPythonApi::IsChanging), R"pbdoc(
      判定 obj 最近是否有更新

        当业务数据更新导致 wait_update 返回后可以使用该函数判断 本次业务数据更新是否包含特定obj或其中某个字段
        关于判断K线更新的说明： 当生成新K线时，其所有字段都算作有更新，若此时执行 api.is_changing(klines.iloc[-1]) 则一定返回True。

      Args:
          obj (any): 任意业务对象, 包括 get_quote 返回的 quote, get_kline_serial 返回的 k_serial, get_account 返回的 account 等

          key (str/list of str): [可选]需要判断的字段，默认不指定

      Returns:
          bool: 如果本次业务数据更新包含了待判定的数据则返回 True, 否则返回 False

     )pbdoc")
    .def("is_changing", py::overload_cast<py::object, py::list>(&TqPythonApi::IsChanging))
    .def("is_changing", py::overload_cast<py::object>(&TqPythonApi::IsChanging))
    .def(
      "get_tick_serial",
      [](py::object& obj, const std::string& symbol, int data_length = 200) {
        auto& api = obj.cast<TqPythonApi&>();
        auto tick = api.GetTickSerial(symbol, data_length);
        return api.GetDataFrame("tick", symbol, tick->m_range_size, static_cast<int>(tick->m_columns.size()),
          tick->m_data, tick->m_columns, obj);
      },
      py::arg("symbol") = "", py::arg("data_length") = 200, R"pbdoc( 获取指定时间段内的 K 线序列.
        请求指定合约的Tick序列数据. 序列数据会随着时间推进自动更新

        Args:
            symbol (str): 指定合约代码

            data_length (int): 需要获取的序列长度。每个序列最大支持请求 8964 个数据

            chart_id (str): [可选]指定序列id, 默认由 api 自动生成

        Returns:
            pandas.DataFrame: 本函数总是返回一个 pandas.DataFrame 实例, 包含以下列:
            - id: 12345 tick序列号

            - datetime: 1501074872000000000 (tick从交易所发出的时间(按北京时间)，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数)

            - last_price: 3887.0 (最新价)

            - average: 3820.0 (当日均价)

            - highest: 3897.0 (当日最高价)

            - lowest: 3806.0 (当日最低价)

            - ask_price1: 3886.0 (卖一价)

            - ask_volume1: 3 (卖一量)

            - bid_price1: 3881.0 (买一价)

            - bid_volume1: 18 (买一量)

            - volume: 7823 (当日成交量)

            - amount: 19237841.0 (成交额)

            - open_interest: 1941 (持仓量)

     )pbdoc")
    .def(
      "get_kline_serial",
      [](py::object& obj, const std::string& symbol, int duration_seconds = 60, int data_length = 200) {
        auto& api = obj.cast<TqPythonApi&>();

        auto klines = api.GetKlineSerial(symbol, duration_seconds, data_length);
        return api.GetDataFrame("kline", symbol + std::to_string(duration_seconds), klines->m_range_size,
          static_cast<int>(klines->m_columns.size()), klines->m_data, klines->m_columns, obj);
      },
      py::arg("symbol") = "", py::arg("duration_seconds") = 60, py::arg("data_length") = 200,
      R"pbdoc( 
        获取tick序列数据

        Args:
          symbol (str): 指定合约代码。当前只支持单个合约

          duration_seconds (int): K 线数据周期, 以秒为单位。例如: 1 分钟线为 60，1 小时线为 3600，日线为 86400。
              注意: 周期在日线以内时此参数可以任意填写, 在日线以上时只能是日线(86400)的整数倍

          data_length (int): 需要获取的序列长度。每个序列最大支持请求 8964 个数据

        Returns:
            pandas.DataFrame: 本函数总是返回一个 pandas.DataFrame 实例。包含以下列:
            - id: 1234 (k线序列号)

            - datetime: 1501074872000000000 (tick从交易所发出的时间(按北京时间)，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数)

            - open: 51450.0 (K线起始时刻的最新价)

            - high: 51450.0 (K线时间范围内的最高价)

            - low: 51450.0 (K线时间范围内的最低价)

            - close: 51450.0 (K线结束时刻的最新价)

            - volume: 11 (K线时间范围内的成交量)

            - open_oi: 27354 (K线起始时刻的持仓量)

            - close_oi: 27355 (K线结束时刻的持仓量)

    )pbdoc")
    .def("get_trading_unit", &TqPythonApi::GetTradingUnits, R"pbdoc( 
      查询交易单元信息.

      Returns:
          返回截止到现在有储存过数据的交易单元列表(有开仓委托但未成交的节点视为未存储过数据).

     )pbdoc")
    .def("_delete_trading_unit", &TqPythonApi::DeleteTradingUnits, py::arg("trading_unit") = ktrade_unit_unset,
      R"pbdoc( 
      删除本地存储的交易节点数据.

      Args:
        trading_unit(int/str): [可选] 计划删除的交易单元编号, 若需删除所有的交易单元, 参数值为 ALL

      )pbdoc")
    .def("query_quotes", &TqPythonApi::QueryQuotes, py::arg("ins_class") = std::string(),
      py::arg("exchange_id") = std::string(), py::arg("product_id") = std::string(), py::arg("expired") = nullptr,
      py::arg("has_night") = nullptr,
      R"pbdoc( 
      根据相应的参数发送合约服务请求查询，并返回查询结果.

      Args:
        ins_class (str): [可选] 合约类型
                                * FUTURE: 期货

                                * CONT: 主连

                                * COMBINE: 组合

                                * INDEX: 指数

                                * OPTION: 期权

                                * STOCK: 股票

        exchange_id (str): [可选] 交易所
                                * CFFEX: 中金所
                                * SHFE: 上期所
                                * DCE: 大商所
                                * CZCE: 郑商所
                                * INE: 能源交易所(原油)
                                * SSE: 上交所
                                * SZSE: 深交所

        product_id (str): [可选] 品种（股票、期权不能通过 product_id 筛选查询）

        expired (bool):   [可选] 是否已下市

        has_night (bool): [可选] 是否有夜盘，默认为 None。
                                * None 表示筛选结果既包括有夜盘品种也包括无夜盘品种
                                * True 表示筛选结果只包括有夜盘品种
                                * False 表示筛选结果只包括无夜盘品种

      Returns:
        list: 符合筛选条件的合约代码的列表，例如: ["SHFE.cu2012", "SHFE.au2012", "SHFE.wr2012"]

      )pbdoc")
    .def("query_cont_quotes", &TqPythonApi::QueryContQuotes, py::arg("exchange_id") = std::string(),
      py::arg("product_id") = std::string(), py::arg("has_night") = nullptr,
      R"pbdoc( 
      根据填写的参数筛选，返回主力连续合约对应的标的合约列表.

      Args:
        exchange_id (str): [可选] 交易所
                                * CFFEX: 中金所
                                * SHFE: 上期所
                                * DCE: 大商所
                                * CZCE: 郑商所
                                * INE: 能源交易所(原油)
                                * SSE: 上交所
                                * SZSE: 深交所

        product_id (str): [可选] 品种（股票、期权不能通过 product_id 筛选查询）

        has_night (bool): [可选] 是否有夜盘，默认为 None。
                                * None 表示筛选结果既包括有夜盘品种也包括无夜盘品种
                                * True 表示筛选结果只包括有夜盘品种
                                * False 表示筛选结果只包括无夜盘品种

      Returns:
        list: 符合筛选条件的合约代码的列表，例如: ["SHFE.cu2012", "SHFE.au2012", "SHFE.wr2012"]

      )pbdoc")
    .def("query_options", &TqPythonApi::QueryOptions, py::arg("underlying_symbol") = std::string(),
      py::arg("option_class") = std::string(), py::arg("exercise_year") = 0, py::arg("exercise_month") = 0,
      py::arg("strike_price") = 0.0, py::arg("expired") = nullptr, py::arg("has_A") = nullptr,
      R"pbdoc( 
      发送合约服务请求查询，查询符合条件的期权列表，并返回查询结果.

      Args:
        underlying_symbol (str):      标的合约

        option_class (str):           [可选] 期权类型
                                            * CALL: 看涨期权
                                            * PUT: 看跌期权

        exercise_year (int):          [可选] 最后行权日年份

        exercise_month (int):         [可选] 最后行权日月份

        strike_price (float):         [可选] 行权价格

        expired (bool):               [可选] 是否下市

        has_A (bool):                 [可选] 是否含有A，输入True代表只含A的期权，输入False代表不含A的期权，默认为None不做区分

        Returns:

            list: 符合筛选条件的合约代码的列表，例如: ["SHFE.cu2012C24000", "SHFE.cu2012P24000"]

      )pbdoc")
    .def("get_trading_status", &TqPythonApi::GetTradingStatus, py::arg("symbol"), R"pbdoc( 
      获取指定合约的交易状态

      Args:
        symbol (str):      合约

      Returns:
        交易状态的引用, 对于每个在交易所交易的品种，它在任意时刻都处于以下三种状态之一.

        * AUCTIONORDERING : 集合竞价报单, 允许用户报单, 报单不会立即成交, 而是等到集合竞价撮合阶段成交

        * CONTINOUS : 连续交易. 主要的交易时段

        * NOTRADING : 非交易时段, 例如午休时间、收盘时间、集合竞价撮合. 不允许用户报单

      Example::

          # 集合竞价报单阶段进行开盘抢单
          from tqsdk2 import TqApi, TqAuth, TqAccount

          account = TqCtp(front_url, front_broker, app_id, auth_code, account_id, password)
          api = TqApi(account = account, auth=TqAuth("信易账户", "账户密码"))
          ts = api.get_trading_status("SHFE.cu2201")
          while True:
            api.wait_update()
            if ts.trade_status == "AUCTIONORDERING":
              order = api.insert_order("SHFE.cu2201","BUY","OPEN", 1, 71400)
              break

          api.close()

      )pbdoc");

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
