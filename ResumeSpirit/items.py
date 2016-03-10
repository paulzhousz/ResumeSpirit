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
    IDtype = scrapy.Field()
    IDNumber = scrapy.Field()
    birthdate = scrapy.Field()
    marital = scrapy.Field()
    phoneNumber = scrapy.Field()
    mobile = scrapy.Field()
    email = scrapy.Field()
    qqNumber = scrapy.Field()
    partisan = scrapy.Field()
    hukou = scrapy.Field()
    address = scrapy.Field()
    degree = scrapy.Field()
    WorkingStart = scrapy.Field()
    currentSalary = scrapy.Field()
    jobStatus = scrapy.Field()
    overseaExp = scrapy.Field()
    overseadesc = scrapy.Field()
    avaliableTime = scrapy.Field()
    jobTime = scrapy.Field()
    expectIndustry = scrapy.Field()
    expectSalary = scrapy.Field()
    category = scrapy.Field()
    eduinfo = scrapy.Field()
    traininginfo = scrapy.Field()
    workexpinfo = scrapy.Field()
    projectinfo = scrapy.Field()
    englishLevel = scrapy.Field()
    japaneselevel = scrapy.Field()
    selfEvaluation = scrapy.Field()
    skill = scrapy.Field()
    postTime = scrapy.Field()
    source = scrapy.Field()
    sourceresumeID = scrapy.Field()
    sourcepositionid = scrapy.Field()
    sourceurl = scrapy.Field()
    status = scrapy.Field()
    createDate = scrapy.Field()
    updateDate = scrapy.Field()
