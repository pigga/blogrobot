#! /usr/bin/env python  
# -*- coding:utf-8 -*-  
# ====#====#====#====
# __author__ = "Yannis"  
# FileName: *.py  
# Version:1.0.0
# ====#====#====#====
import sys
import logging
from blogrobot.utils.readconfig import read_node_by_config
reload(sys)
sys.setdefaultencoding('utf-8')


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger(object):

    def __init__(self, log_name, log_format_temp, logger):
        # if os.path.exists(log_name):
        #     pass
        # else:
        #     os.chmod('/var/log', stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        #     with open(log_name, 'w'):
        #         pass
        """
           指定保存日志的文件路径，日志的输出样式，以及调用文件
           将日志存入到指定的文件中
        """

        # 用字典保存日志级别
        format_dict = {
            1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        }

        log_level_str = read_node_by_config("log_level")
        if log_level_str is None:
            log_level = logging.NOTSET
        elif log_level_str.lower() == "critical":
            log_level = logging.CRITICAL
        elif log_level_str.lower() == "error":
            log_level = logging.ERROR
        elif log_level_str.lower() == "warning":
            log_level = logging.WARNING
        elif log_level_str.lower() == "info":
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(log_level)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name)
        fh.setLevel(log_level)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        # 定义handler的输出格式
        formatter = format_dict[int(log_format_temp)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
