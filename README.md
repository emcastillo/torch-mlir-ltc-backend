# Motivation

When trying to add a backend for a device in torch-mlir using the [LazyTensorCore
backend](https://github.com/llvm/torch-mlir/blob/main/docs/ltc_backend.md),
 it can be troublesome to compile using a toolchain for your device.

This repository provides an unmodified version of
 [torch-mlir reference ltc backend](https://github.com/llvm/torch-mlir/tree/main/python/torch_mlir/csrc/reference_lazy_backend)
 that can be compiled and imported standalone. Note that the sources are unaltered copies from the corresponding
torch-mlir ones with only the `CMakeLists.txt` file modified to be an independent project.

# Compile

Download and build torch-mlir
```
$ git clone https://github.com/llvm/torch-mlir
$ cd torch-mlir
$ git submodule update --init
$ cmake -GNinja -Bbuild \
  -DCMAKE_BUILD_TYPE=Release \
  -DPython3_FIND_VIRTUALENV=ONLY \
  -DLLVM_ENABLE_PROJECTS=mlir \
  -DLLVM_EXTERNAL_PROJECTS="torch-mlir;torch-mlir-dialects" \
  -DLLVM_EXTERNAL_TORCH_MLIR_SOURCE_DIR="$PWD" \
  -DLLVM_EXTERNAL_TORCH_MLIR_DIALECTS_SOURCE_DIR="$PWD"/externals/llvm-external-projects/torch-mlir-dialects \
  -DMLIR_ENABLE_BINDINGS_PYTHON=ON \
  -DLLVM_TARGETS_TO_BUILD=host \
  externals/llvm-project/llvm
$ cmake --build build --target tools/torch-mlir/all
```
clone this repo

build with
```
$ cmake -Bbuild . -DTORCH_MLIR_DIR=../torch-mlir
$ cmake --build build
```

# Execute

```
$ export PYTHONPATH=`pwd`/build/python_packages/torch_mlir/
$ python test.py
```
