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
    site_url = "http://new.o-hr.cn"
    login_url = "http://new.o-hr.cn/user/ajax/ajaxLogin"
    position_list_url = "http://new.o-hr.cn/user/job/ajaxGetJobs"
    position_detail_url_prefix = "http://new.o-hr.cn/jobs/detail/"
    resume_list_url = "http://new.o-hr.cn/user/job/ajaxGetUser"
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
        # 定义职位列表页面第一页 POST Form Data
        #: s=1:当前生效职位
        #: s=100:所有发布职位
        #: c_page:当前页
        #: t_page:下一页页数
        self.position_formdata = {
            "s": "1",
            "c_page": "0",
            "t_page": "1",
        }
        #: 构造获取简历列表第一页 post form data
        #: jobid:职位ID
        #: c_page:当前页
        #: t_page:下一页页数
        #: type:"apply"
        self.resumelist_fromdata = {
            "jobid": "",
            "c_page": "0",
            "t_page": "1",
            "type": "apply"
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
        # self.log("get position list result=" + positon_data['result'])
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
                for key in item.keys():
                    item[key] = ""

                item["sourcepositionid"] = position_code
                item["branchid"] = self.branch_id
                item["status"] = "1"
                item["source"] = "OHR"

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
        positionitem = response.meta["position_item"]
        positionitem["sourceurl"] = response.url
        #: 职位名称
        position_name = sel.xpath('//div[@class="title"]/text()').extract_first(default="")
        # self.log(position_name)
        positionitem["positionname"] = position_name.strip()
        # self._log_page(response, position_name + ".html")

        #: 薪资信息
        salary = sel.xpath('//div[@class="salary"]/text()').extract_first(default="")
        # self.log(salary)
        positionitem["salary"] = salary.strip()

        #: 工作地点&工作经验
        text = sel.xpath('//div[@class="location"]/text()').extract()
        location = text[0].strip() if text[0] else ""
        experience = text[1].strip() if text[1] else ""
        exp = re.sub(r'\D+', "", experience)
        if exp == "":
            exp = "0"
        positionitem["location"] = location
        positionitem["experience"] = exp

        #: 截止时间
        text = sel.xpath('//div[@class="posttime"]/text()').extract_first(default="")
        if text != "":
            enddate = text.strip()[-10:]
        else:
            enddate = ""
        # self.log(enddate)
        positionitem["enddate"] = enddate

        basic_info = sel.xpath('//div[@class="basic-info info-group"]/ul/li/text()').extract()
        #: 职位类别
        try:
            positionitem["category"] = basic_info[0]
        except Exception:
            positionitem["category"] = ""

        #: 工作性质
        try:
            positionitem["workingtime"] = basic_info[1]
        except Exception:
            positionitem["workingtime"] = ""

        #: 招聘人数
        try:
            positionitem["hiringnumber"] = basic_info[2]
        except Exception:
            positionitem["hiringnumber"] = ""

        #: 所属部门
        try:
            positionitem["department"] = basic_info[3]
        except Exception:
            positionitem["department"] = ""

        #: 汇报对象
        try:
            positionitem["reportto"] = basic_info[4]
        except Exception:
            positionitem["reportto"] = ""

        #: 下属人数
        try:
            positionitem["managecount"] = basic_info[5]
        except Exception:
            positionitem["managecount"] = ""

        #: 岗位要求
        positiondesc = sel.xpath('//li[@class="long"]/text()').extract()
        desc = ""
        for p in positiondesc:
            desc = desc + p
        # self.log(desc)
        positionitem["positiondesc"] = desc

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
                positionitem["degree"] = info
            #: 性别要求
            elif label.find(u"性别要求") != -1:
                positionitem["sex"] = info
            #: 语言要求
            elif label.find(u"语言要求") != -1:
                #: 使用空格分隔语言和等级
                infol = info.split("\t")
                # self.log(infol)
                positionitem["language"] = infol[0]
                positionitem["languagelevel"] = infol[1]
            #: 专业要求
            elif label.find(u"专业要求") != -1:
                positionitem["major"] = info
            #: 年龄要求
            elif label.find(u"年龄要求") != -1:
                infol = re.findall(r'\d+', info)
                positionitem["agefrom"] = infol[0]
                positionitem["ageto"] = infol[1]
            i += 1
        # self.log(item)
        # yield positionitem

        #: 获取简历列表数据
        position_code = positionitem["sourcepositionid"]
        self.resumelist_fromdata["jobid"] = position_code
        yield FormRequest(
            self.resume_list_url,
            meta={
                "cookiejar": response.meta["cookiejar"],
                "positioncode": position_code, },
            callback=self.parse_resumelist,
            method="POST",
            headers=self.headers,
            formdata=self.resumelist_fromdata,
        )

    #: parse_resumelist(self,response)
    #: 处理返回的简历列表json数据
    def parse_resumelist(self, response):
        resume_data = json.loads(response.body)
        if resume_data['result'] == "SUCCESS":
            sel = Selector(text=resume_data["data"])
            # self.log(resume_data["data"])
            #: 获取简历列表页数
            resume_page_number = self.get_pageNumber(sel)
            #: 处理第一页的简历信息url
            resume_url_list = sel.xpath('//a[contains(@href,"/user/resume/detail/")]/@href').extract()
            i = 0
            while i < len(resume_url_list):
                resumeitem = ResumeItem()
                for key in resumeitem.keys():
                    resumeitem[key] = ""
                urls = resume_url_list[i]
                #: 处理简历详细页面url
                resume_url = self.site_url + urls.split("'")[1]
                # self.log(resume_url)
                #: 获取简历投递日期
                datepath = '//table//tr[' + str(i + 2) + ']/td[6]/text()'
                post_time = sel.xpath(datepath).extract_first()
                resumeitem["source"] = "OHR"
                resumeitem["postTime"] = post_time
                resumeitem["sourcepositionid"] = response.meta["positioncode"]
                #: 抓取简历详细页面
                yield FormRequest(
                    resume_url,
                    meta={
                        "cookiejar": response.meta["cookiejar"],
                        "resume_item": resumeitem,
                    },
                    callback=self.parse_resumedata,
                    headers=self.headers,
                )
                i += 1
                #: 处理下一页数据
            if resume_page_number > 1:
                for cpage in range(1, resume_page_number):
                    self.resumelist_fromdata["c_page"] = str(cpage)
                    self.resumelist_fromdata["t_page"] = str(cpage + 1)
                    self.resumelist_fromdata["jobid"] = response.meta["positioncode"]
                    yield FormRequest(
                        self.resume_list_url,
                        meta={
                            "cookiejar": response.meta["cookiejar"],
                            "positioncode": self.resumelist_fromdata["jobid"], },
                        callback=self.parse_resumelist,
                        method="POST",
                        headers=self.headers,
                        formdata=self.resumelist_fromdata,
                    )

    #: parse_resumedata(self,response)
    #: 处理简历详细页面
    def parse_resumedata(self, response):
        sel = Selector(response)
        resume_item = response.meta["resume_item"]
        resume_item["sourceurl"] = response.url
        # 中文姓名
        cname = sel.xpath('//div[@class="user_name"]/text()').extract_first(default="")
        resume_item["cname"] = cname
        # 英文姓名
        ename = ""
        resume_item["ename"] = ename
        # 性别
        sex = sel.xpath('//div[@class="fs14"]/text()').extract_first(default="")
        resume_item["sex"] = sex
        # 居住城市
        residence = sel.xpath('//div[@class="tag"]/text()').extract_first(default="")
        resume_item["residence"] = residence

        # 基本资料 begin
        # 表格第1行
        # 证件类型
        IDtype = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[1]/td[2]/text()').extract_first(default="")
        # self.log(IDtype)
        resume_item["IDtype"] = IDtype
        # 证件号
        IDNumber = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[1]/td[4]/text()').extract_first(default="")
        # self.log(IDNumber)
        resume_item["IDNumber"] = IDNumber

        # 表格第2行
        # 出生年月
        birthdate = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[2]/td[2]/text()').extract_first(default="")
        birthdate = birthdate[:7]
        # self.log(birthdate)
        resume_item["birthdate"] = birthdate
        # 婚姻状况
        marital = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[2]/td[4]/text()').extract_first(default="")
        # self.log(marital)
        resume_item["marital"] = marital

        # 表格第3行
        # 手机号码
        mobile = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[3]/td[2]/text()').extract_first(default="")
        # self.log(mobile)
        resume_item["mobile"] = mobile
        # 家庭电话
        phoneNumber = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[3]/td[4]/text()').extract_first(default="")
        # self.log(phoneNumber)
        resume_item["phoneNumber"] = phoneNumber

        # 表格第4行
        # 邮箱
        email = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[4]/td[2]/text()').extract_first(default="")
        # self.log(email)
        resume_item["email"] = email
        # QQ
        qqNumber = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[4]/td[4]/text()').extract_first(default="")
        # self.log(qqNumber)
        resume_item["qqNumber"] = qqNumber

        # 表格第5行
        # 党派
        partisan = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[5]/td[2]/text()').extract_first(default="")
        # self.log(partisan)
        resume_item["partisan"] = partisan
        # 户口
        hukou = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[5]/td[4]/text()').extract_first(default="")
        # self.log(hukou)
        resume_item["hukou"] = hukou

        # 表格第6行
        # 地址
        address = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[6]/td[2]/text()').extract_first(default="")
        # self.log(address)
        resume_item["address"] = address

        # 表格第7行
        # 学历
        degree = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[7]/td[2]/text()').extract_first(default="")
        # self.log(degree)
        resume_item["degree"] = degree
        # 工作起始年
        workingstart = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[7]/td[4]/text()').extract_first(default="")
        # self.log(WorkingStart)
        resume_item["WorkingStart"] = workingstart

        # 表格第8行
        # 目前年薪
        currentSalary = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[8]/td[2]/text()').extract_first(default="")
        # self.log(currentSalary)
        resume_item["currentSalary"] = currentSalary

        # 表格第9行
        # 求职状态
        jobStatus = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[9]/td[2]/text()').extract_first(default="")
        # self.log(jobStatus)
        resume_item["jobStatus"] = jobStatus
        # 海外经验
        overseaExp = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[9]/td[4]/text()').extract_first(default="")
        # self.log(overseaExp)
        resume_item["overseaExp"] = overseaExp

        # 表格第10行
        # 海外经历
        overseadesc = sel.xpath('//div[@id="p_info_view"]/table/tbody/tr[10]/td[2]/text()').extract_first(
            default="")
        # self.log(overseadesc)
        resume_item["overseadesc"] = overseadesc
        # 基本资料 end

        # 求职意向 begin
        # 表格第1行
        # 到岗时间
        avaliableTime = sel.xpath('//div[@id="p_want_view"]/table/tbody/tr[1]/td[2]/text()').extract_first(
            default="")
        # self.log(avaliableTime)
        resume_item["avaliableTime"] = avaliableTime

        # 表格第2行
        # 工作性质
        jobTime = sel.xpath('//div[@id="p_want_view"]/table/tbody/tr[2]/td[2]/text()').extract_first(
            default="")
        # self.log(jobTime)
        resume_item["jobTime"] = jobTime

        # 表格第3行
        # 期望行业
        expectIndustry = sel.xpath('//div[@id="p_want_view"]/table/tbody/tr[3]/td[2]/text()').extract_first(
            default="")
        # self.log(expectIndustry)
        resume_item["expectIndustry"] = expectIndustry

        # 表格第4行
        # 期望年薪
        expectSalary = sel.xpath('//div[@id="p_want_view"]/table/tbody/tr[4]/td[2]/text()').extract_first(
            default="")
        # self.log(expectSalary)
        resume_item["expectSalary"] = expectSalary

        # 表格第5行
        # 目标职能
        category = sel.xpath('//div[@id="p_want_view"]/table/tbody/tr[5]/td[2]/text()').extract_first(
            default="")
        # self.log(category)
        resume_item["category"] = category
        # 求职意向 end

        # 教育背景 begin
        schoollist = sel.xpath('//dt[@class="school_nav"]/span/text()').extract()
        for i 
        s1=sel.xpath('//div[@id="p_edu1_view"]/dl/div[3]/div/text()').extract()
        # //*[@id="p_edu1_view"]/dl/dt/span 学校名称
        # //*[@id="p_edu1_view"]/dl/dt/text() 时间
        # //*[@id="p_edu1_view"]/dl/div[1]/span 学历
        # //*[@id="p_edu1_view"]/dl/div[2]/span 专业
        # //*[@id="p_edu1_view"]/dl/div[3]/div 描述
        self.log(schoollist)
        # 教育背景 end
        # self.log(resume_item)

    #: get_pageNumber(self, selector):
    #: 从返回的html中获取数据页数
    #: 如果发生异常，返回-1
    #: selector:Selector实例
    def get_pageNumber(self, selector):
        try:
            page_num_str = selector.xpath('//a[@class="mr10 ls1"]/text()').re(r'\d+')[0]
            page_num = int(page_num_str)
        except Exception:
            page_num = -1
        finally:
            return page_num
