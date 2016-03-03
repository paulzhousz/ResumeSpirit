#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ResumeInfo(Base):
    __tablename__ = "t_resumeinfo"
    resumeid = Column(String(50), primary_key=True)
    cname = Column(String(20))
    ename = Column(String(20))
    sex = Column(String(10))
    idtype = Column(String(20))
    idnumber = Column(String(50))
    birthdate = Column(String(20))
    marital = Column(String(10))
    phonenumber = Column(String(20))
    mobile = Column(String(20))
    email = Column(String(50))
    qqnumber = Column(String(50))
    partisan = Column(String(100))
    hukou = Column(String(100))
    address = Column(String(100))
    degree = Column(String(50))
    currentsalary = Column(String(50))
    jobstatus = Column(String(50))
    overseaexp = Column(String(10))
    avaliabletime = Column(String(20))
    jobtime = Column(String(10))
    expectindustry = Column(String(100))
    expectsalary = Column(String(100))
    category = Column(String(100))
    englishlevel = Column(String(100))
    selfevaluation = Column(String(500))
    skill = Column(String(500))
    posttime = Column(String(30))
    source = Column(String(20))
    sourceresumeid = Column(String(50))
    status = Column(String(10))
    createdate = Column(String(30))
    updatedate = Column(String(30))
