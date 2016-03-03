#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BranchInfo(Base):
    __tablename__ = "t_branchinfo"

    branchid = Column(String(50))
    cname = Column(String(100))
    ename = Column(String(100))
    createdate = Column(String(30))
    updatedate = Column(String(30))
