#! /usr/bin/env python
# -*- coding:utf-8 -*-
# ====#====#====#====
# __author__ = "Yannis"
# FileName: *.py
# Version:1.0.0
# ====#====#====#====
import requests
import json
from blogrobot.utils.readconfig import read_node_by_config
import sys
from blogrobot.utils.log import Logger

log_path = read_node_by_config("log_path")
logInfo = Logger(log_name=log_path, log_format_temp=1, logger='HttpClient').get_log()
reload(sys)
sys.setdefaultencoding('utf-8')


class HttpClient(object):

    default_headers = {"Content-type": "application/json"}

    def __init__(self):
        pass

    @staticmethod
    def get(url, params=None, req_headers=None):
        if req_headers is None:
            req_headers = HttpClient.default_headers
        try:
            r = requests.get(url=url, params=params, headers=req_headers)
            r.encoding = 'utf-8'
            return r.text
        except BaseException as e:
            logInfo.error("get request error ,errorMsg : %s" % str(e))
        except requests.exceptions.ConnectTimeout as e:
            logInfo.error("the connection of get request is down,please check it. the error message is : %s" % str(e))
        except requests.exceptions.Timeout as e:
            logInfo.error("the get request time out,the error message is : %s" % str(e))
        except requests.exceptions.HTTPError as e:
            logInfo.error('the get request failed, the error message is : %s' % str(e))
        return None

    @staticmethod
    def post(url, data_dict=None, req_headers=None, files=None):
        if req_headers is None:
            req_headers = HttpClient.default_headers
        data = None
        if data_dict is not None:
            data = json.dumps(data_dict)
        try:
            r = requests.post(url=url, data=data, headers=req_headers, files=files)
            r.encoding = 'utf-8'
            return r.text
        except BaseException as e:
            logInfo.error("post request error ,errorMsg : %s" % str(e))
        except requests.exceptions.ConnectTimeout as e:
            logInfo.error("the connection of post request is down,please check it. the error message is : %s" % str(e))
        except requests.exceptions.Timeout as e:
            logInfo.error("the post request time out,the error message is : %s" % str(e))
        except requests.exceptions.HTTPError as e:
            logInfo.error('the post request failed, the error message is : %s' % str(e))
        return None

    @staticmethod
    def put(url, data_dict=None, req_headers=None):
        if req_headers is None:
            req_headers = HttpClient.default_headers
        data = None
        if data_dict is not None:
            data = json.dumps(data_dict)
        try:
            r = requests.put(url=url, data=data, headers=req_headers)
            r.encoding = 'utf-8'
            return r.text
        except BaseException as e:
            logInfo.error("put request error ,errorMsg : %s" % str(e))
        except requests.exceptions.ConnectTimeout as e:
            logInfo.error("the connection of put request is down,please check it. the error message is : %s" % str(e))
        except requests.exceptions.Timeout as e:
            logInfo.error("the put request time out,the error message is : %s" % str(e))
        except requests.exceptions.HTTPError as e:
            logInfo.error('the put request failed, the error message is : %s' % str(e))
        return None

    @staticmethod
    def delete(url, data_dict=None, req_headers=None):
        if req_headers is None:
            req_headers = HttpClient.default_headers
        data = None
        if data_dict is not None:
            data = json.dumps(data_dict)
        try:
            r = requests.delete(url=url, data=data, headers=req_headers)
            r.encoding = 'utf-8'
            return r.text
        except BaseException as e:
            logInfo.error("delete request error ,errorMsg : %s" % str(e))
        except requests.exceptions.ConnectTimeout as e:
            logInfo.error("the connection of delete request is down,please check it. the error message is : %s" % str(e))
        except requests.exceptions.Timeout as e:
            logInfo.error("the delete request time out,the error message is : %s" % str(e))
        except requests.exceptions.HTTPError as e:
            logInfo.error('the delete request failed, the error message is : %s' % str(e))
        return None
