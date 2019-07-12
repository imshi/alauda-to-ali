#!/usr/bin/python
# coding=utf-8
# ###############
# 定义公共函数及部分全局变量（在该脚本尾部）
# ###############
import subprocess
import os
import time


# 定义公共函数
def dir_verify(path_name):
    if not os.path.exists(path_name):
        os.makedirs(path_name)

# 定义部分全局变量
ali_registry = "registry-vpc.cn-hangzhou.aliyuncs.com/ecarx-app/"
app_yaml_dir = os.path.join(os.getcwd(),"yaml")
app_j2_dir = os.path.join(os.getcwd(),"template")
j2_tempalte = 'app_deployment.j2'
app_namespace = "default"

# 父目录
# os.path.abspath(os.path.dirname(os.getcwd()))
