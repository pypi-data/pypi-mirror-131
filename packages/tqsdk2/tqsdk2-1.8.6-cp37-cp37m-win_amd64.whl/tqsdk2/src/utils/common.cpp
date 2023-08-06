/*******************************************************************************
 * @file parameter_check.h
 * @brief 参数校验公共函数
 * @copyright 上海信易信息科技股份有限公司 版权所有
 ******************************************************************************/
#include "common.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

#pragma warning(disable : 4996)
std::string NowAsString() {
  char buf[100] = {0};
  std::time_t now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
  std::strftime(buf, sizeof(buf), "%Y%m%d%H%M%S ", std::localtime(&now));
  return buf;
}

std::filesystem::path exe_path() {
#ifdef _WIN32
  wchar_t buffer[MAX_PATH_LENGTH] = {0};
  GetModuleFileNameW(NULL, buffer, MAX_PATH_LENGTH);
  std::filesystem::path pexe = buffer;
#else
  char buffer[MAX_PATH_LENGTH];
  ssize_t count = readlink("/proc/self/exe", buffer, MAX_PATH_LENGTH);
  std::filesystem::path pexe = std::string(buffer, (count > 0) ? count : 0);
#endif
  return pexe.parent_path();
}

int GetPID() {
#ifdef _WIN32
  return GetCurrentProcessId();
#else
  return getpid();
#endif
}

std::string TrimSymbol(const std::string& symbol) {
  auto ReplaceChars = [](std::string str, const std::string& from, const std::string& to) {
    size_t start_pos = 0;
    while ((start_pos = str.find(from, start_pos)) != std::string::npos) {
      str.replace(start_pos, from.length(), to);
      start_pos += to.length();
    }
    return str;
  };

  return ReplaceChars(ReplaceChars(symbol, ".", "_"), "@", "_");
}

std::string EpochNanoToHumanTime(int64_t nano) {
  auto dt = EpochNanoToLocalDateTime(nano);

  char buf[32] = {0};
  snprintf(buf, 32, "%04d-%02d-%02d %02d:%02d:%02d.%06d", dt.date_time.tm_year + 1900, dt.date_time.tm_mon + 1,
    dt.date_time.tm_mday, dt.date_time.tm_hour, dt.date_time.tm_min, dt.date_time.tm_sec,
    static_cast<int>(dt.nano_seconds / 1000));
  return std::string(buf);
}

std::string GetDateStr(int64_t nano) {
  auto dt = EpochNanoToLocalDateTime(nano);

  char buf[45];
  snprintf(buf, 45, "%04d-%02d-%02d", dt.date_time.tm_year + 1900, dt.date_time.tm_mon + 1, dt.date_time.tm_mday);
  return std::string(buf);
}

void TqSyncRequest(std::shared_ptr<TqApi> tqapi, std::shared_ptr<UserCommand> request) {
  py::gil_scoped_release release;
  tqapi->AsyncRequest(request);
  while (request->status != UserCommand::Status::kFinished) {
    tqapi->RunOnce();
  }
  py::gil_scoped_acquire acquire;
}

bool DoubleEqual(double d1, double d2) {
  return std::fabs(d1 - d2) < 0.000001;
}

void RunUntilReady(std::shared_ptr<TqApi> api, std::function<bool(void)> func, int time_out) {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  while (!func()) {
    if (std::chrono::steady_clock::now() - start > std::chrono::seconds(time_out))
      throw std::exception(std::logic_error("接收数据超时，请检查客户端及网络是否正常."));
    py::gil_scoped_release release;
    api->RunOnce();
    py::gil_scoped_acquire a;
  }
}
