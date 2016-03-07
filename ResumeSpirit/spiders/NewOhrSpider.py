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

import re

from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy import Selector

from ResumeSpirit.items import PositionItem, ResumeItem


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

    def __init__(self, branch_id="1", ohr_username="天臣国际", ohr_pwd="123456", *args, **kwargs):
        super(NewOhrSpider, self).__init__(*args, **kwargs)
        self.branch_id = branch_id
        # 定义登录页面 POST Form Data
        self.login_formdata = {
            "company": "1",
            "username": ohr_username,
            "password": ohr_pwd,
            "captcha": ""
        }
        # 定义职位列表页面 POST Form Data
        #: s=1:当前生效职位
        #: s=100:所有发布职位
        #: c_page:当前页
        #: t_page:下一页页数
        self.position_formdata = {
            "s": "1",
            "c_page": "0",
            "t_page": "1",
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
        # self.log("login result=" + login_data['result'])

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

    #: parse_positionlist(self, response):
    #: 处理返回的职位列表json数据
    def parse_positionlist(self, response):
        positon_data = json.loads(response.body)
        #self.log("get position list result=" + positon_data['result'])
        if positon_data['result'] == "SUCCESS":
            # self.log(positon_data["data"])
            sel = Selector(text=positon_data["data"])
            #: 获取职位列表页数
            position_page_number = self.get_pageNumber(sel)
            #: 处理第一页的职位信息url
            positonid_list = sel.xpath('//a[contains(@href,"/job/index/")]/@href').re(r'\d+')
            self.log(positonid_list)
            for position_code in positonid_list:
                position_data_url = self.position_detail_url_prefix + position_code
                item = PositionItem()
                item["sourcepositionid"] = position_code
                item["branchid"] = self.branch_id
                item["status"] = "1"
                item["source"] = "OHR"
                item["positionid"] = ""
                item["positionname"] = ""
                item["hiringnumber"] = ""
                item["location"] = ""
                item["workingtime"] = ""
                item["degree"] = ""
                item["sex"] = ""
                item["language"] = ""
                item["languagelevel"] = ""
                item["agefrom"] = ""
                item["ageto"] = ""
                item["experience"] = ""
                item["category"] = ""
                item["major"] = ""
                item["salary"] = ""
                item["positiondesc"] = ""
                item["enddate"] = ""
                item["reportto"] = ""
                item["managecount"] = ""
                item["department"] = ""
                item["sourceurl"] = ""
                item["createdate"] = ""
                item["updatedate"] = ""
                item["resumes"] = []
                yield FormRequest(
                    position_data_url,
                    meta={
                        "cookiejar": response.meta["cookiejar"],
                        "position_item": item,
                    },
                    callback=self.parse_positiondata,
                    headers=self.headers,
                )
            #: 处理下一页数据
            if position_page_number > 1:
                for cpage in range(1, position_page_number):
                    self.position_formdata["c_page"] = str(cpage)
                    self.position_formdata["t_page"] = str(cpage + 1)
                    yield FormRequest(
                        self.position_list_url,
                        meta={"cookiejar": response.meta["cookiejar"]},
                        callback=self.parse_positionlist,
                        method="POST",
                        headers=self.headers,
                        formdata=self.position_formdata,
                    )
                    # self.log("complete!")

    def parse_positiondata(self, response):
        sel = Selector(response)
        item = response.meta["position_item"]
        item["sourceurl"] = response.url
        #: 职位名称
        position_name = sel.xpath('//div[@class="title"]/text()').extract_first(default="")
        # self.log(position_name)
        item["positionname"] = position_name.strip()
        # self._log_page(response, position_name + ".html")

        #: 薪资信息
        salary = sel.xpath('//div[@class="salary"]/text()').extract_first(default="")
        # self.log(salary)
        item["salary"] = salary.strip()

        #: 工作地点&工作经验
        text = sel.xpath('//div[@class="location"]/text()').extract()
        location = text[0].strip() if text[0] else ""
        experience = text[1].strip() if text[1] else ""
        exp = re.sub(r'\D+', "", experience)
        if exp == "":
            exp = "0"
        item["location"] = location
        item["experience"] = exp

        #: 截止时间
        text = sel.xpath('//div[@class="posttime"]/text()').extract_first(default="")
        if text != "":
            enddate = text.strip()[-10:]
        else:
            enddate = ""
        # self.log(enddate)
        item["enddate"] = enddate

        basic_info = sel.xpath('//div[@class="basic-info info-group"]/ul/li/text()').extract()
        #: 职位类别
        try:
            item["category"] = basic_info[0]
        except Exception:
            item["category"] = ""

        #: 工作性质
        try:
            item["workingtime"] = basic_info[1]
        except Exception:
            item["workingtime"] = ""

        #: 招聘人数
        try:
            item["hiringnumber"] = basic_info[2]
        except Exception:
            item["hiringnumber"] = ""

        #: 所属部门
        try:
            item["department"] = basic_info[3]
        except Exception:
            item["department"] = ""

        #: 汇报对象
        try:
            item["reportto"] = basic_info[4]
        except Exception:
            item["reportto"] = ""

        #: 下属人数
        try:
            item["managecount"] = basic_info[5]
        except Exception:
            item["managecount"] = ""

        #: 岗位要求
        positiondesc = sel.xpath('//li[@class="long"]/text()').extract()
        desc = ""
        for p in positiondesc:
            desc = desc + p
        # self.log(desc)
        item["positiondesc"] = desc

        require_label = sel.xpath('//div[@class="required-info info-group"]/ul/li/label/text()').extract()
        require_info = sel.xpath('//div[@class="required-info info-group"]/ul/li/text()').extract()
        # self.log(item["sourcepositionid"])
        # self.log(require_label)
        # self.log(require_info)
        i = 0
        while i < len(require_label):
            label = require_label[i]
            info = require_info[i]
            # self.log(item["sourcepositionid"]+"-"+label)
            # self.log(item["sourcepositionid"]+"-"+info)
            #: 学历要求
            if label.find(u"学历要求") != -1:
                item["degree"] = info
            #: 性别要求
            elif label.find(u"性别要求") != -1:
                item["sex"] = info
            #: 语言要求
            elif label.find(u"语言要求") != -1:
                #: 使用空格分隔语言和等级
                infol = info.split("\t")
                # self.log(infol)
                item["language"] = infol[0]
                item["languagelevel"] = infol[1]
            #: 专业要求
            elif label.find(u"专业要求") != -1:
                item["major"] = info
            #: 年龄要求
            elif label.find(u"年龄要求") != -1:
                infol = re.findall(r'\d+', info)
                item["agefrom"] = infol[0]
                item["ageto"] = infol[1]
            i += 1
        # self.log(item)
        yield item

    #: get_pageNumber(self, selector):
    #: 从返回的html中获取数据页数
    #: 如果发生异常，返回-1
    #: selector:Selector实例
    def get_pageNumber(self, selector):
        try:
            page_num_str = selector.xpath('//a[@class="mr10 ls1"]/value()').re(r'\d+')[0]
            page_num = int(page_num_str)
        except Exception:
            page_num = -1
        finally:
            return page_num
