/*******************************************************************************
 * @file binding.cpp
 * @brief 做市商模块python绑定
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "market_maker.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void BindingTqMarketMaker(py::module_& m) {
  py::class_<TqMarketMaker>(m, "TqMarketMaker")
    .def(py::init<py::object, const std::string&>(), py::arg("api"), py::arg("symbol"), R"pbdoc( 
      天勤期货做市商策略模板.

      创建做市商策略实例.

      Args:
        api (TqApi):      [必选] TqApi实例，该做市商策略依托于指定api实例
        symbol (str):     [必选] 做市标的合约
     )pbdoc")
    .def_property_readonly("status", &TqMarketMaker::GetStatus, R"pbdoc( 
      当前做市策略的运行状态. 

      Values:
        **NOT_RUNNING**:  策略未运行;

        **RUNNING**: 策略运行中;

        **PAUSE**:  策略暂停, 当策略暂停条件不满足时，策略会继续运行, 执行挂单操作. 导致策略暂停的原因包括但不局限以下原因:

            * 挂单成交, 暂停N秒
            * 单边市不报价
            * 盘口价宽超过指定阈值
            * 市场价格接近涨跌停
            * 净持仓超过阈值
            * 平仓亏损超过阈值
            * 超出做市时间范围

        具体原因可以通过 status_msg 获取.

     )pbdoc")
    .def_property_readonly("status_msg", &TqMarketMaker::GetStatusMsg, R"pbdoc( 
      获取当前做市策略的运行状态信息.
     )pbdoc")
    .def("cancel", &TqMarketMaker::Stop, py::arg("reason") = std::string(), R"pbdoc( 
      停止做市商策略的运行.

      停止做市商策略并对挂单进行撤单. 

      Args:
        reason (str):     [可选] 做市商策略停止原因

     )pbdoc")
    .def("set_market_maker", &TqMarketMaker::SetMarketMakerConfig, R"pbdoc( 
      设置做市报价参数.

      动态设置做市商参数, 设置完成后的策略将在下一次的 wait_update() 中被执行. 
      
      Args:
        **quote_spread (int):**   [必填] 报价价差. 单位 "跳", 即合约的最小价格变动单位.

        **quote_volume (int):**   [必填] 报价挂单手数. 在场上买卖双方均维持此手数的挂单.

        **time_range(list)**     [必填] 做市时间段, 格式为 [('091000', '101000'), ('103500', '112500'), ('210000', '250000')...], 每两个数字定义一个可以做市的时间段.

        **quote_spread_2 (int):** [可选] 第二组报价价差. 默认值 0.

        **quote_volume_2 (int):** [可选] 第二组报价手数. 默认值 0.

        **min_position_volume (int):** [可选] 最小持仓数量限制. 默认值 0 .

        **bid_min_volume (int):** [可选] 最小买一量. 买一量小于此值时, 买单价格后退一个价位, 设为 0 则不使用此机制, 默认值 0. 

        **ask_min_volume (int):** [可选] 最小卖一量. 卖一量小于此值时, 卖单价格后退一个价位, 设为 0 则不使用此机制, 默认值 0.

        **use_quote_command (boolean):**   [可选] 是否使用交易所做市报价指令. 默认值 False.

        **spread_limit (int):**  [可选] 价差阙值. 单位为"跳", 即合约的最小价格变动单位. 当市场买卖价差超过此值时, 暂停做市报价. 默认值为 100.

        **price_limit (int):**   [可选] 停板阙值. 单位为"跳", 即合约的最小价格变动单位. 当买卖价距离涨跌停小于此值时, 暂停做市报价. 默认值为1.

        **net_position_limit (int):**    [可选] 净持仓限制, 做市合约净持仓手数超过此值时, 暂停做市报价. 默认值 100 手.

        **close_profit_limit (float):**  [可选] 平仓亏损限制, 做市合约当日累积平仓盈亏超过此值时, 暂停做市报价. 例如,设置为 10000, 表示亏损超过10000时暂停做市.默认值为 10000 .

        **pause_seconds_when_trade (float):**  [可选] 做市挂单成交暂停时长(秒).当做市挂单有任意成交时, 撤销所有做市挂单, 等待 N 秒后再重新挂单. 若N==0, 则做市挂单一直维持在场上.默认值为 0.

        **run_hedge (boolean):**  [可选] 用户是否要求执行对冲流程, 做市挂单成交时发出对冲报单. 默认值为 False.

        **hedge_instrument_id (str):**  [可选] 对冲合约. 若未设定, 则使用报价合约.

        **hedge_order_max_price_adjust(int):**     [可选] 对冲单最大报单价格调整. hedge_price_adjust 的单位为"跳", 即合约的最小价格变动单位.

                                                     - 当 hedge_price_adjust == 0 时, 对冲单的报单价格等于做市挂单的成交价.

                                                     - 当 hedge_price_adjust > 0 时, 对冲单的报单价格向有利于成交的方向调整.

                                                     - 当 hedge_price_adjust < 0 时, 对冲单的报单价格向不利于成交的方向调整.

                                                     * example:
                                                     * CFFEX.IF2101 合约的最小价格变动单位为 0.2. 假定它的一个做市买单在 3020.0 的价格成交了1手, 则:
                                                     * 若 hedge_price_adjust == 0, 则对冲单为 3020.0 卖出 1 手
                                                     * 若 hedge_price_adjust == 1, 则对冲单为 3019.8 卖出 1 手 （向利于成交的方向移动1个价位)
                                                     * 若 hedge_price_adjust == -3, 则对冲单为 3020.6 卖出 1 手 （向不利于成交的方向移动3个价位)
     )pbdoc");
}