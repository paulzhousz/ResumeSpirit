#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

'''
从新版OHR（http://new.o-hr.cn/）网站模拟用户登录，抓取发布的职位信息及投递的简历信息
******************************************************************************
1.创建时间：2016/2/21
******************************************************************************
'''

import json
import logging
import scrapy

from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy import Selector


class NewOhrSpider(Spider):
    login_url = "http://new.o-hr.cn/user/ajax/ajaxLogin"
    position_list_url = "http://new.o-hr.cn/user/job/ajaxGetJobs"
    position_detail_url_prefix = "http://new.o-hr.cn/jobs/detail/"
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
        return [FormRequest(
            self.login_url,
            meta={"cookiejar": 1},
            callback=self.post_login,
            method="POST",
            headers=self.headers,
            formdata=self.login_formdata,
        )]

    def post_login(self, response):
        login_data = json.loads(response.body)
        self.log("login result=" + login_data['result'])

        # 返回SUCCESS，登录成功
        if login_data['result'] == "SUCCESS":
            self.log("login success!")
            return [FormRequest(
                self.position_list_url,
                meta={"cookiejar": response.meta["cookiejar"]},
                callback=self.parse_positionlist,
                method="POST",
                headers=self.headers,
                formdata=self.position_formdata,
            )]
        else:
            self.log("login failed!", level=logging.ERROR)

    # 处理返回的职位列表json数据
    def parse_positionlist(self, response):
        positon_data = json.loads(response.body)
        self.log("get position list result=" + positon_data['result'])
        if positon_data['result'] == "SUCCESS":
            # self.log(positon_data["data"])
            sel = Selector(text=positon_data["data"])
            # 处理第一页的职位信息url
            positonid_list = sel.xpath('//a[contains(@href,"/jobs/detail")]/@href').re(r'\d+')
            self.log(positonid_list)
            for position_id in positonid_list:
                position_data_url = self.position_detail_url_prefix + position_id
                yield FormRequest(
                    position_data_url,
                    meta={"cookiejar": response.meta["cookiejar"]},
                    callback=self.parse_positiondata,
                    headers=self.headers,
                )
            self.log("complete!")

    def parse_positiondata(self, response):
        sel = Selector(response)
        positon_name = sel.xpath('//div[@class="title"]/text()').extract()
        # self.log("position name:"+positon_name[0])
        self._log_page(response, positon_name[0] + ".html")

    # 从返回的html中获取数据页数
    # 如果发生异常，返回-1
    def get_pageNumber(self, responsebody):
        try:
            selector_text = Selector(text=responsebody)
            page_num_str = selector_text.xpath('//a[@class="mr10 ls1"]/text()').re(r'\d+')[0]
            page_num = int(page_num_str)
        except Exception:
            page_num = -1
        finally:
            return page_num
