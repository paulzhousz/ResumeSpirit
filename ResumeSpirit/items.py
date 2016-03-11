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
    resumes = scrapy.Field()
    createdate = scrapy.Field()
    updatedate = scrapy.Field()


class ResumeItem(scrapy.Item):
    resumeID = scrapy.Field()
    cname = scrapy.Field()
    ename = scrapy.Field()
    sex = scrapy.Field()
    residence = scrapy.Field()
    idtype = scrapy.Field()
    idnumber = scrapy.Field()
    birthdate = scrapy.Field()
    marital = scrapy.Field()
    phonenumber = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    qqnumber = scrapy.Field()
    partisan = scrapy.Field()
    hukou = scrapy.Field()
    address = scrapy.Field()
    degree = scrapy.Field()
    workingstart = scrapy.Field()
    currentsalary = scrapy.Field()
    jobstatus = scrapy.Field()
    overseaexp = scrapy.Field()
    overseadesc = scrapy.Field()
    avaliabletime = scrapy.Field()
    jobtime = scrapy.Field()
    expectindustry = scrapy.Field()
    expectsalary = scrapy.Field()
    category = scrapy.Field()
    eduinfo = scrapy.Field()
    traininginfo = scrapy.Field()
    workexpinfo = scrapy.Field()
    projectexpinfo = scrapy.Field()
    englishlevel = scrapy.Field()
    japaneselevel = scrapy.Field()
    selfevaluation = scrapy.Field()
    skill = scrapy.Field()
    posttime = scrapy.Field()
    source = scrapy.Field()
    sourceresumeid = scrapy.Field()
    sourcepositionid = scrapy.Field()
    sourceurl = scrapy.Field()
    status = scrapy.Field()
    createdate = scrapy.Field()
    updatedate = scrapy.Field()
