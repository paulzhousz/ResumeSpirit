#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, "app.db"))
    DEBUG = True
