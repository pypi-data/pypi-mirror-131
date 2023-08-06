//
// Created by 徐秋实 on 2021/12/9.
//

#ifndef LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
#define LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
#include <unordered_map>
#include "pybind11/pybind11.h"
#include "boost/asio/io_service.hpp"
#include "boost/bind.hpp"
#include "boost/thread/thread.hpp"
#include "boost/asio/thread_pool.hpp"
#include "boost/progress.hpp"

namespace py = pybind11;
namespace encoders {
class LabelEncoder {
 public:
  std::unordered_map<std::string, int> encoder_map;

 public:
  LabelEncoder();
  /// 使用一个一维字符串列表进行fit
  /// \param string_vector
  /// \param n_worker
  void encode1D(const std::vector<std::string> &string_vector, int n_worker = 1);

  /// 将一个一维字符串transform
  /// \param string_vector
  /// \param n_worker
  std::vector<int> transform1D(const std::vector<std::string> &string_vector, int n_worker = 1);

 private:
  /// 将多个子结果即每个进程处理的结果, 整合起来更新encoder_map
  /// \param results 每个进程的处理结果
  /// \param start_end_points 每一个结果的开始结束index
  void combineEncodeThreadResults(
      const std::vector<std::unordered_map<std::string, int>> &results,
      const std::vector<std::pair<u_long, u_long>> &start_end_points
  );

 private:
  /// 将长度等分成工人数
  /// \param length 总长度
  /// \param n_worker 工人数
  /// \return 每一个值为分组的起点与重点，左闭右闭
  static std::vector<std::pair<u_long, u_long>> split1DListByWorkers(u_long length, int n_worker);

  /// 给定一个字符串列表，并给定起始位置，获取编码结果
  /// \param string_vector 需要编码的列表
  /// \param start_end_point 开始与结束位置
  /// \param result_map 结果map
  /// \param bar 进度条
  /// \return
  static void singleThreadEncode1d(
      const std::vector<std::string> &string_vector,
      const std::pair<u_long, u_long> &start_end_point,
      std::unordered_map<std::string, int> &result_map,
      boost::progress_display &bar
  );

  /// 将给定的字符串列表, 进行编码
  /// \param string_vector 输入字符串列表
  /// \param start_end_point 分割后的开始结束位置
  /// \param result_vector 结果列表
  /// \param bar 进度
  static void singleThreadTransform1d(
      const std::unordered_map<std::string, int> &encoder_map,
      const std::vector<std::string> &string_vector,
      const std::pair<u_long, u_long> &start_end_point,
      std::vector<int> &result_vector,
      boost::progress_display &bar
  );
};
}
#endif //LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
