/*******************************************************************************
 * @file backtest.cpp
 * @brief TqSDK2 回测类
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "backtest.h"

BackTest::BackTest(timestamp start_dt, timestamp end_dt) {
  m_service = md::BackTestService::Create(start_dt.time_since_epoch().count(), end_dt.time_since_epoch().count());
}

std::shared_ptr<BackTestService> BackTest::GetService() {
  return m_service;
}