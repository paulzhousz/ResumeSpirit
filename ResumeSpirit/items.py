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
    pid = scrapy.Field()
    name = scrapy.Field()
    start_date = scrapy.Field()
    End_date = scrapy.Field()
    status = scrapy.Field()
    source = scrapy.Field()


class ResumeItem(scrapy.Item):
    rid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
