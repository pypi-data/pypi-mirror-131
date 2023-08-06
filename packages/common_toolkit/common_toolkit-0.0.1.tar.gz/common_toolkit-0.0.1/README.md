# Common Toolkit
通用的`python`工具包

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Git hook: pre-commit](https://img.shields.io/badge/git%20hook-pre--commit-orange)](https://github.com/PyCQA/flake8)
[![Release: flit](https://img.shields.io/badge/release-flit-green)](https://github.com/pypa/flit)

## 1、说明
`common_toolkit`包含以下几部分功能，可按需加载不同功能包的依赖模块（参考3）

- cli: ,安装本包会同时扩展一些shell命令，详细介绍如下
    - `py`
        - 说明：在当前目录创建python项目骨架相关命令
        - 使用：`$py --help`
- development: 常见python开发相关的工具包
- penetration: 渗透测试相关功能包

## 2、安装
```shell script
pip install common_toolkit
```

## 3、依赖按需加载
eg1: 只想要使用开发相关的依赖
```shell script
pip install "common_toolkit[development]"
```
eg2: 只想要使用渗透测试相关的依赖
```shell script
pip install "common_toolkit[penetration]"
```
eg3: 如果需要使用两个及以上相关的依赖，请在中括号中用`,`将需要安装的依赖包名分隔
```shell script
pip install "common_toolkit[development,penetration]"
```
