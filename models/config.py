#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = 'Paul'

'''
    SQLAlchemy初始化
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "app.db"))
engine = create_engine(db_url)
db_session = sessionmaker(bind=engine)
