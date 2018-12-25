#! /usr/bin/env python  
# -*- coding:utf-8 -*-  
# ====#====#====#====
# __author__ = "Yannis"  
# FileName: *.py  
# Version:1.0.0
# ====#====#====#====

"""读取配置文件内的相关节点"""
import yaml


def read_node_by_config(node_name):
    # 解析配置文件及对应节点
    file_path = '../initconfig.yaml'
    f = open(file_path)
    s = yaml.load(f)
    current_node = s[node_name]
    return current_node
