# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

sourceDict = {
    '0': 'OHR',
    '1': '51Job'}


class PositionItem(scrapy.Item):
    positionid = scrapy.Field()
    positionname = scrapy.Field()
    hiringnumber = scrapy.Field()
    location = scrapy.Field()
    workingtime = scrapy.Field()
    degree = scrapy.Field()
    sex = scrapy.Field()
    language = scrapy.Field()
    languagelevel = scrapy.Field()
    agefrom = scrapy.Field()
    ageto = scrapy.Field()
    experience = scrapy.Field()
    category = scrapy.Field()
    major = scrapy.Field()
    salary = scrapy.Field()
    positiondesc = scrapy.Field()
    enddate = scrapy.Field()
    source = scrapy.Field()
    sourcepositionid = scrapy.Field()
    status = scrapy.Field()
    branchid = scrapy.Field()
    reportto = scrapy.Field()
    managecount = scrapy.Field()
    department = scrapy.Field()
    sourceurl = scrapy.Field()
    createdate = scrapy.Field()
    updatedate = scrapy.Field()


class ResumeItem(scrapy.Item):
    rid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
