#! /usr/bin/env python  
# -*- coding:utf-8 -*-  
# ====#====#====#====
# __author__ = "Yannis"  
# FileName: *.py  
# Version:1.0.0
# ====#====#====#====
import re
from blogrobot.utils.readconfig import read_node_by_config
import sys
from bs4 import BeautifulSoup
from blogrobot.utils.httputils import HttpClient
from blogrobot.utils.log import Logger
log_path = read_node_by_config("log_path")
logInfo = Logger(log_name=log_path, log_format_temp=1, logger='HttpUtils').get_log()
reload(sys)
sys.setdefaultencoding('utf-8')


class CnBlogs(object):

    def __init__(self):
        pass

    @classmethod
    def get_blog_info_and_content(cls):
        req_url = read_node_by_config("cnblogs_url")
        req_header = {'User-Agent':
                      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        temp_post_info_list = []
        # 默认先获取第一页
        get_post_info(req_url, req_header, 1, temp_post_info_list)
        for temp_post_info in temp_post_info_list:
            get_post_content_info(req_header, temp_post_info)


def get_post_content_info(req_header, temp_post_info):
    req_response = HttpClient.get(temp_post_info['url'], req_headers=req_header)
    print req_response
    post_content = BeautifulSoup(req_response, 'lxml')
    post_title = post_content.find('a', id='cb_post_title_url').text.strip()
    post_content = post_content.find('div', id='cnblogs_post_body').text.strip()
    print post_title
    print post_content


def get_post_info(req_url, req_header, page_index, temp_post_info_list):
    req_params = {"page": page_index}
    req_response = HttpClient.get(req_url, req_params, req_header)
    page = BeautifulSoup(req_response, 'lxml')
    items = page.find_all('div', class_='post')
    for post_item in items:
        temp_post_item = {}
        # 仅获取界面的相关博客内容
        content_str = post_item.find('div', class_='postFoot').text.strip()
        temp_content_arr = content_str.split(" ")
        temp_post_item['url'] = post_item.find("a").get("href")
        temp_post_item['date'] = temp_content_arr[2] + " " + temp_content_arr[3]
        temp_post_item['read_num'] = int(re.findall('\((.*?)\)', temp_content_arr[5])[0])
        temp_post_item['post_num'] = int(re.findall('\((.*?)\)', temp_content_arr[6])[0])
        temp_post_info_list.append(temp_post_item)
    # TODO 开发注释掉该部分代码
    # if len(items) == 10:
    #     get_post_info(req_url, req_header, page_index + 1, temp_post_info_list)



CnBlogs.get_blog_info_and_content()

