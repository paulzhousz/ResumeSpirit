#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PositionResume(Base):
    __tablename__ = "t_positionresume"

    id = Column(String(50), primary_key=True)
    positionid = Column(String(50))
    resumeid = Column(String(50))
    createdate = Column(String(30))
    updatedate = Column(String(30))
