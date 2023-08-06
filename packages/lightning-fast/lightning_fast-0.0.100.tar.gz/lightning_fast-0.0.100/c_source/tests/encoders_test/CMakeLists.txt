include_directories(../../external_include)
include_directories(../../encoders)

add_executable(encoders_test main_test.cpp label_encoder_test.cpp label_encoder_test.h)

target_link_libraries(encoders_test encoders CONAN_PKG::boost)