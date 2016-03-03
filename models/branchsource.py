#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BranchSource(Base):
    __tablename__ = "t_branchsource"

    branchsourceid = Column(String(50))
    branchid = Column(String(50))
    sourceid = Column(String(50))
    companyname = Column(String(50))
    username = Column(String(50))
    passwordset = Column(String(100))
    createdate = Column(String(30))
    updatedate = Column(String(30))
