# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import uuid
from sqlalchemy import and_
from models import config
from models.positioninfo import PositionInfo
from models.resumeinfo import ResumeInfo


class ResumespiritPipeline(object):
    def open_spider(self, spider):
        self.session = config.db_session()

    def process_item(self, item, spider):
        source = item["source"]
        positioncode = item["sourcepositionid"]

        position = self.session.query(PositionInfo).filter(
            and_(PositionInfo.source == source,
                 PositionInfo.sourcepositionid == positioncode
                 ))
        if position:

        return item

    def close_spider(self, spider):
        self.session.close()
