/*******************************************************************************
 * @file backtest_report.cpp
 * @brief 回测报表信息
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "backtest_report.h"

#include <algorithm>
#include <numeric>
#include <pybind11/pybind11.h>
#include "fclib/accout_his_query_service.h"
#include "../field_mapping.h"
#include "../utils/common.h"

#undef max
#undef min

namespace py = pybind11;

void ProfitReportParser::DefineStruct(Trade& d) {
  AddItem(d.seq_no, ("seqno"));
  AddItem(d.user_id, ("user_id"));
  AddItem(d.exchange_id, ("exchange_id"));
  AddItem(d.instrument_id, ("instrument_id"));
  AddItem(d.order_id, ("order_id"));
  AddItem(d.exchange_trade_id, ("exchange_trade_id"));
  AddItem(d.exchange_order_id, ("order_id"));
  AddItemEnum(d.direction, ("direction"),
    {
      {Direction::kBuy, ("kBuy")},
      {Direction::kSell, ("kSell")},
    });
  AddItemEnum(d.offset, ("offset"),
    {
      {Offset::kOpen, ("kOpen")},
      {Offset::kClose, ("kClose")},
      {Offset::kCloseToday, ("kCloseToday")},
    });
  AddItem(d.volume, ("volume"));
  AddItem(d.price, ("price"));
  AddItem(d.trade_date_time, ("trade_date_time"));
  AddItem(d.commission, ("commission"));
  d.hedge_flag = OrderHedgeFlag::kSpeculation;
}

void ProfitReportParser::DefineStruct(Account& d) {
  AddItem(d.investor_id, ("user_id"));
  AddItem(d.currency, ("currency"));
  AddItem(d.pre_balance, ("pre_balance"));
  AddItem(d.deposit, ("deposit"));
  AddItem(d.withdraw, ("withdraw"));
  AddItem(d.close_profit, ("close_profit"));
  AddItem(d.commission, ("commission"));
  AddItem(d.premium, ("premium"));
  AddItem(d.position_profit, ("position_profit"));
  AddItem(d.float_profit, ("float_profit"));
  AddItem(d.balance, ("balance"));
  AddItem(d.margin, ("margin"));
  AddItem(d.frozen_margin, ("frozen_margin"));
  AddItem(d.frozen_commission, ("frozen_commission"));
  AddItem(d.frozen_premium, ("frozen_premium"));
  AddItem(d.available, ("available"));
  AddItem(d.risk_ratio, ("risk_ratio"));
  AddItem(d.option_market_value, ("market_value"));
}

/************************************************************************/
/* 盈亏报告                                                              */
/************************************************************************/
ProfitReport::ProfitReport()
  : finished(false)
  , annual_yield(0.0)
  , balance(0.0)
  , loss_value(0.0)
  , loss_volumes(0.0)
  , max_drawdown(0.0)
  , profit_loss_ratio(0.0)
  , profit_value(0.0)
  , profit_volumes(0.0)
  , ror(0.0)
  , sharpe_ratio(0.0)
  , winning_rate(0.0){};

ProfitReport& ProfitReport::GeneratorReport(std::vector<double> daily_yield) {
  winning_rate = (profit_volumes + loss_volumes) ? profit_volumes / (profit_volumes + loss_volumes) : 0;  // 胜率

  // 盈亏额比例
  auto loss_pre_volume = loss_volumes ? loss_value / loss_volumes : 0;
  auto profit_pre_volume = profit_volumes ? profit_value / profit_volumes : 0;
  profit_loss_ratio = loss_pre_volume ? std::abs(profit_pre_volume / loss_pre_volume) : 0;

  // 收益率
  auto _ror = balance / init_balance;
  ror = _ror - 1;

  // 年化收益率
  annual_yield = daily_yield.size() ? (std::pow(_ror, (250 / daily_yield.size())) - 1) : 0;

  // 计算夏普率
  double sum = std::accumulate(std::begin(daily_yield), std::end(daily_yield), 0.0);
  double mean = sum / daily_yield.size();  //均值
  double accum = 0.0;
  std::for_each(std::begin(daily_yield), std::end(daily_yield), [&](const double d) {
    accum += (d - mean) * (d - mean);
  });
  double stdev = std::sqrt(accum / (daily_yield.size() - 1));  //方差
  sharpe_ratio = stdev ? std::pow(250, 0.5) * (mean - 0.0001) / stdev : 0;

  finished = true;
  return *this;
}

std::string ProfitReport::ToString() {
  std::stringstream s;
  s << "胜率:" << (winning_rate * 100.00) << "%, 盈亏额比例:" << profit_loss_ratio << ", 收益率:" << (ror * 100.00)
    << "%, 年化收益率:" << (annual_yield * 100.00) << "%, 最大回撤:" << (max_drawdown * 100.00)
    << "%, 年化夏普率:" << sharpe_ratio;

  return s.str();
}

BacktestReport::BacktestReport(
  std::shared_ptr<TqApi> api, bool disable_print, std::string user_key, double init_balance)
  : m_api(api)
  , m_disable_print(disable_print)
  , m_user_key(user_key) {
  m_his_service = m_api->GetHisRecordService();
  m_report = std::make_shared<ProfitReport>();
  m_report->init_balance = init_balance;
}

std::shared_ptr<ProfitReport> BacktestReport::GetReport() {
  // 成交记录统计
  GetTradesRecord();

  // 资产明细统计
  GetAccountRecords();

  // 统计盈亏手数
  CulProfitLoss();

  m_report->GeneratorReport(m_daily_yield);
  if (!m_disable_print) {
    py::print(m_report->ToString());
  }

  return m_report;
}

void BacktestReport::GetTradesRecord() {
  auto all = m_his_service->GetAccountHisRecords(StringToEpochNano("1970/01/01"), StringToEpochNano("2099/12/31"));

  if (!m_disable_print)
    py::print(" INFO - 模拟交易成交记录");

  auto trade_records = m_his_service->GroupingHisRecords(all, GroupType::kTradingDay,
    [&](const future::AccountHisRecord& boundary, const future::AccountHisRecord& record) -> bool {
      return record.record_type == RecordType::kTrade;
    });

  for (auto& record : trade_records) {
    for (auto& r : record.records) {
      if (r.record_type == RecordType::kTrade) {
        ProfitReportParser ss;
        ss.FromString(r.record_content.c_str());
        rapidjson::Value& datas = (*ss.m_doc)["trade"];
        Trade t;
        ss.ToVar(t, &datas);

        if (t.offset == Offset::kOpen) {
          m_open_trades.push_back(t);
        } else {
          m_close_trades.push_back(t);
        }

        //输出成交信息
        if (!m_disable_print) {
          auto date_time = EpochNanoToHumanTime(t.trade_date_time);
          std::stringstream trade_notify;
          trade_notify << " INFO - 时间: " << date_time << ", 合约: " << t.symbol() << ", 开平:" << GetOffSet(t.offset)
                       << ", 方向:" << GetDirection(t.direction) << ", 手数:" << t.volume << ", 价格:" << t.price
                       << ", 手续费:" << t.commission;

          py::print(trade_notify.str());
        }
      }
    }
  }
}

void BacktestReport::GetAccountRecords() {
  // 成交记录统计
  if (!m_disable_print)
    py::print(" INFO - 模拟交易账户资金");

  double max_balance = 0.0;  // 资金最高值, 用于计算最大回测
  auto all = m_his_service->GetAccountHisRecords(StringToEpochNano("1970/01/01"), StringToEpochNano("2099/12/31"));
  auto is_first = true;
  auto account_record = m_his_service->FilterLastInEachGroup(all, GroupType::kTradingDay,
    [&](const future::AccountHisRecord& boundary, const future::AccountHisRecord& record) -> bool {
      if (record.record_type == RecordType::kSnap) {
        if (is_first) {
          is_first = false;
          return false;
        }

        ProfitReportParser parser;
        parser.FromString(record.record_content.c_str());
        rapidjson::Value& datas = (*parser.m_doc)["snaps"][m_user_key]["account"];
        Account account;
        parser.ToVar(account, &datas);

        max_balance = std::max(max_balance, account.balance);
        m_report->max_drawdown =
          std::max(m_report->max_drawdown, (max_balance - account.balance) / max_balance);  // 最大回测
        m_report->balance = account.balance;

        m_daily_yield.push_back(account.balance / account.pre_balance - 1);  // 每日收益率

        //输出每日盈亏信息
        if (!m_disable_print) {
          auto date = GetDateStr((*parser.m_doc)["datetime"].GetInt64());
          std::stringstream notify;
          notify << std::fixed << " INFO - 日期: " << date << ", 账户权益: " << account.balance
                 << ", 可用资金:" << account.available << ", 浮动盈亏:" << account.float_profit
                 << ", 持仓盈亏:" << account.position_profit << ", 平仓盈亏:" << account.close_profit
                 << ", 市值:" << account.option_market_value << ", 保证金:" << account.margin
                 << ", 手续费:" << account.commission << ", 风险度:" << account.risk_ratio;

          py::print(notify.str());
        }

        return true;
      }
      return false;
    });

  return;
}

void BacktestReport::CulProfitLoss() {
  for (auto& close : m_close_trades) {
    auto volume_multiple = m_api->DataDb()->GetNode<md::Instrument>(close.symbol())->Snap()->volume_multiple;
    auto opposite_direction = close.direction == Direction::kSell ? Direction::kBuy : Direction::kSell;
    auto cur_close_volume = close.volume;

    for (auto& open : m_open_trades) {
      if (open.symbol() != close.symbol() || open.direction != opposite_direction)
        continue;

      auto matched_volume = std::min(cur_close_volume, open.volume);
      cur_close_volume -= matched_volume;
      open.volume -= matched_volume;
      // 平仓盈亏
      auto profit = close.direction == Direction::kSell ? (close.price - open.price) : (open.price - close.price);
      if (profit >= 0) {
        m_report->profit_volumes += matched_volume;                           // 盈利手数
        m_report->profit_value += profit * matched_volume * volume_multiple;  // 盈利金额
      } else {
        m_report->loss_volumes += matched_volume;                           // 亏损手数
        m_report->loss_value += profit * matched_volume * volume_multiple;  // 亏损金额
      }
    }
  }
}
