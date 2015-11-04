#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

"""
    模拟用户操作，抓取o-hr网站的用户有效职位及已投递简历
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest


class OhrSpider(CrawlSpider):
    name = "ohr"
    allowed_domains = ["www.o-hr.cn"]
    start_urls = [
        "http://www.o-hr.cn/cms/jobadmin.php"
    ]
    rules = ()
    cook = {
        "PHPSESSID": "ae3bac668e577e158292d696c15ffbf3"
    }
    headers = {
        "Host": "www.o-hr.cn",
        "Connection": "keep-alive",
        # Content-Length: 67
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Origin": "http://www.o-hr.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://www.o-hr.cn/recruit/e_user.php",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        # "Cookie": "PHPSESSID=ae3bac668e577e158292d696c15ffbf3"
    }

    def __init__(self, *a, **kw):
        super(OhrSpider, self).__init__(*a, **kw)
        self.after_login = None

    def start_requests(self):
        return [Request("http://www.o-hr.cn/recruit/e_user.php", meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        print(u'登陆准备...')
        # 获取页面中form的hidden域sc_user的值
        sc_user = Selector(response).xpath('//input[@name="sc_user"]/@value').extract()[0]
        print 'sc_user=', sc_user
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,  # "http://www.o-hr.cn/recruit/e_user.php",
                                          # meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,
                                          formdata={
                                              'sc_user': sc_user,
                                              'submit': u'提交',
                                              'pfc_username': u'天臣国际',
                                              'pfc_password': '123456'
                                          },
                                          cookies=self.cook,
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def _log_page(self, response, filename):  # 这个函数主要作用是把页面抓下来，因为某些登录后的页面用scrapy shell调试很麻烦也方便你查看登录页面需要提交的表单
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))

    def parse(self, response):
        self._log_page(response, 'after_login.html')
