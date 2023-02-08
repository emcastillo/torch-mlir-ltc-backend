cmake_minimum_required(VERSION 3.4)

if(POLICY CMP0074)
  cmake_policy(SET CMP0074 NEW)
endif()
project(pfvm-ltc-backend LANGUAGES CXX C)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

if(NOT DEFINED TORCH_MLIR_DIR)
 message(FATAL_ERROR "You must set -DTORCH_MLIR_DIR option")
endif()

if(NOT DEFINED TORCH_MLIR_BUILD_DIR)
 message(WARNING "Setting TORCH_MLIR_BUILD_DIR to ${TORCH_MLIR_DIR}/build")
 set(TORCH_MLIR_BUILD_DIR "${TORCH_MLIR_DIR}/build")
endif()

set(TORCH_MLIR_PYTHON_PACKAGES_DIR "${CMAKE_CURRENT_BINARY_DIR}/python_packages")
set(LIBRARY_OUTPUT_PATH  "${TORCH_MLIR_PYTHON_PACKAGES_DIR}/torch_mlir/torch_mlir/_mlir_libs")
set(OUTPUT_NAME "_REFERENCE_LAZY_BACKEND")

# set(Python_ADDITIONAL_VERSIONS 3)
find_package(Python3 COMPONENTS Interpreter Development)

# Find torch installation
list(APPEND CMAKE_MODULE_PATH "${TORCH_MLIR_DIR}/python/torch_mlir/cmake/modules")
include(TorchMLIRPyTorch)

TorchMLIRProbeForPyTorchInstall()
find_package(Torch 2.0 REQUIRED)

include_directories(BEFORE
        ${TORCH_INCLUDE_DIRS}
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
        ${TORCH_MLIR_BUILD_DIR}
        ${TORCH_MLIR_BUILD_DIR}/include
        ${TORCH_MLIR_BUILD_DIR}/tools/torch-mlir/include
        ${TORCH_MLIR_BUILD_DIR}/tools/mlir/include/
        ${TORCH_MLIR_DIR}/
        ${TORCH_MLIR_DIR}/include
        ${TORCH_MLIR_DIR}/python
        ${TORCH_MLIR_DIR}/externals/llvm-project/mlir/include
        ${TORCH_MLIR_DIR}/externals/llvm-project/llvm/include/
        ${Python3_INCLUDE_DIRS}
        ${PYTHON_H_DIR}
        )

list(APPEND CMAKE_MODULE_PATH "${TORCH_MLIR_BUILD_DIR}/lib/cmake/mlir")
include(MLIRDetectPythonEnv)
mlir_detect_pybind11_install()
find_package(pybind11 REQUIRED)

link_directories("${TORCH_INSTALL_PREFIX}/lib")
link_directories(${TORCH_MLIR_BUILD_DIR}/lib)
link_directories(${TORCH_MLIR_BUILD_DIR}/tools/torch-mlir/python_packages/torch_mlir/torch_mlir/_mlir_libs)
add_link_options(-Wl,-rpath,$ORIGIN/lib)

add_library(reference_lazy_backend MODULE
        backend_impl.cpp
        reference_lazy_backend_pybind.cpp
        )

target_link_libraries(reference_lazy_backend
        ${TORCH_LIBRARIES}
        torch_python
        _torch_mlir_ltc
        )

message(STATUS "TORCH_CXXFLAGS=${TORCH_CXXFLAGS} -Wno-pedantic")
set_target_properties(reference_lazy_backend PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${LIBRARY_OUTPUT_PATH}
        OUTPUT_NAME ${OUTPUT_NAME}
        PREFIX "${PYTHON_MODULE_PREFIX}"
        SUFFIX "${PYTHON_MODULE_EXTENSION}"
        CXX_VISIBILITY_PRESET "hidden"
        COMPILE_FLAGS "${TORCH_CXXFLAGS} -Wno-pedantic"
        )
