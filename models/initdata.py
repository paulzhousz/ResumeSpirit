#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date :'3/3/16 23:07'
__author__ = 'paul'

from models import config, sourcesiteinfo
import uuid
import datetime

session = config.db_session()
site_ohr = sourcesiteinfo.SourcesiteInfo(
    sourceid=str(uuid.uuid1()),
    code="OHR",
    name="OHR",
    createdate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
session.add(site_ohr)
session.commit()
session.close()
