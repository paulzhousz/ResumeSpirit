#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from scrapy import cmdline

cmdline.execute("scrapy crawl {spider name}".split())
