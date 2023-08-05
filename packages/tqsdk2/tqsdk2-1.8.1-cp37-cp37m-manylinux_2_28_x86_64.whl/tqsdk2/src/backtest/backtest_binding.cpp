/*******************************************************************************
 * @file binding.cpp
 * @brief 回测模块python绑定
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "backtest.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void BindingBacktest(py::module_& m) {
  // 自定义异常，当回测结束后会抛出 BacktestFinished 例外
  static py::exception<BacktestFinished> ex(m, "BacktestFinished");
  py::register_exception_translator([](std::exception_ptr p) {
    try {
      if (p)
        std::rethrow_exception(p);
    } catch (const BacktestFinished& e) {
      ex(e.what());
    }
  });

  py::class_<BackTest>(m, "TqBacktest")
    .def(py::init<timestamp, timestamp>(), py::arg("start_dt"), py::arg("end_dt"), R"pbdoc( 
      天勤2 回测类

      将该类传入 TqApi 的构造函数, 则策略就会进入回测模式。

      Args:

        start_dt (datetime): 回测起始时间, 如果类型为 date 则指的是交易日, 如果为 datetime 则指的是具体时间点
        end_dt (datetime):   回测结束时间, 如果类型为 date 则指的是交易日, 如果为 datetime 则指的是具体时间点

     )pbdoc");
}