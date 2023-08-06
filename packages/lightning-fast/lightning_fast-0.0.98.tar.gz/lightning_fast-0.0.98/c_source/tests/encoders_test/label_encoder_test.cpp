//
// Created by 徐秋实 on 2021/12/13.
//
#include <cstdlib>
#include <random>
#include "label_encoder_test.h"
void LabelEncoderTest::basic_test() {
  int max_length = 1000;
  srand(222); // NOLINT(cert-msc51-cpp)
  std::vector<std::string> sample_chars = {"赵", "钱", "孙", "李", "周", "吴", "郑", "王"};
  u_long char_count = sample_chars.size();
  std::vector<std::string> sample_words = std::vector<std::string>();
  for (int i = 0; i < max_length; i++) {
    std::string tmp_word = sample_chars[(int) (rand()) % char_count] // NOLINT(cert-msc50-cpp)
        + sample_chars[(int) (rand()) % char_count] // NOLINT(cert-msc50-cpp)
        + sample_chars[(int) (rand()) % char_count]; // NOLINT(cert-msc50-cpp)
    sample_words.push_back(tmp_word);
  }
  auto test_encoder = encoders::LabelEncoder();
  test_encoder.encode1D(sample_words, 3);
  auto transform_result = test_encoder.transform1D(sample_words);
}
