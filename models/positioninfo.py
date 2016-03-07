#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PositionInfo(Base):
    __tablename__ = "T_PositionInfo"

    positionID = Column(String(50), primary_key=True)
    positionname = Column(String(100))
    hiringnumber = Column(Integer)
    location = Column(String(50))
    workingtime = Column(String(20))
    degree = Column(String(20))
    sex = Column(String(10))
    language = Column(String(20))
    languagelevel = Column(String(10))
    agefrom = Column(Integer)
    ageto = Column(Integer)
    experience = Column(Integer)
    category = Column(String(100))
    major = Column(String(100))
    salary = Column(String(100))
    positiondesc = Column(String(2000))
    enddate = Column(String(20))
    source = Column(String(20))
    sourcepositionid = Column(String(50))
    sourceurl = Column(String(200))
    status = Column(String(10))
    branchid = Column(String(50))
    createdate = Column(String(30))
    updatedate = Column(String(30))
