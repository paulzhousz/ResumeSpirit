#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "t_userinfo"
    userid = Column(String(50), primary_key=True)
    loginname = Column(String(20))
    username = Column(String(20))
    passwordset = Column(String(100))
    branchid = Column(String(50))
    isadmin = Column(String(10))
    isenabled = Column(String(10))
    createdate = Column(String(30))
    updatedate = Column(String(30))
