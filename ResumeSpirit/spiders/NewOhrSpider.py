#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

'''
从新版OHR（http://new.o-hr.cn/）网站模拟用户登录，抓取发布的职位信息及投递的简历信息
******************************************************************************
1.创建时间：2016/2/21
******************************************************************************
'''

from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
import json, logging
from scrapy.http import Request, FormRequest


class NewOhrSpider(Spider):
    login_url = "http://new.o-hr.cn/user/ajax/ajaxLogin"
    position_url = "http://new.o-hr.cn/user/job/ajaxGetJobs"
    name = "newohr"
    allowed_domains = ["new.o-hr.cn"]

    # 这个函数主要作用是把抓取整个页面
    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))

    def __init__(self, ohr_username="天臣国际", ohr_pwd="123456", *args, **kwargs):
        super(NewOhrSpider, self).__init__(*args, **kwargs)

        # 定义登录页面 POST Form Data
        self.login_formdata = {
            "company": "1",
            "username": ohr_username,
            "password": ohr_pwd,
            "captcha": ""
        }
        # 定义职位列表页面 POST Form Data
        # s=1:当前生效职位
        # s=100:所有发布职位
        self.position_formdata = {
            "s": "1",
        }
        self.headers = {
            "Host": "new.o-hr.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "http://new.o-hr.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36",
            "Referer": "http://new.o-hr.cn/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
        }

    def start_requests(self):
        self.log(self.login_formdata)
        # 模拟用户登录
        yield FormRequest(
            self.login_url,
            meta={"cookiejar": 1},
            callback=self.post_login,
            method='POST',
            headers=self.headers,
            formdata=self.login_formdata,
        )

    def post_login(self, response):
        data = json.loads(response.body)
        self.log("result=" + data['result'])

        # 返回SUCCESS，登录成功
        if data['result'] == "SUCCESS":
            self.log("login success!")
        else:
            self.log("login failed!", level=logging.ERROR)
