# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import uuid
from datetime import date, datetime
from sqlalchemy import and_
from models import config
from models.positioninfo import PositionInfo
from models.resumeinfo import ResumeInfo


class ResumespiritPipeline(object):

    def open_spider(self, spider):
        self.session = config.db_session()

    def process_item(self, item, spider):
        # logging.info(item.__dict__)
        position_entity = PositionInfo()
        position_entity.positionname = item["positionname"]
        position_entity.hiringnumber = item["hiringnumber"]
        position_entity.location = item["location"]
        position_entity.workingtime = item["workingtime"]
        position_entity.degree = item["degree"]
        position_entity.sex = item["sex"]
        position_entity.language = item["language"]
        position_entity.languagelevel = item["languagelevel"]
        position_entity.agefrom = item["agefrom"]
        position_entity.ageto = item["ageto"]
        position_entity.experience = item["experience"]
        position_entity.category = item["category"]
        position_entity.major = item["major"]
        position_entity.salary = item["salary"]
        position_entity.positiondesc = item["positiondesc"]
        position_entity.enddate = item["enddate"]
        position_entity.source = item["source"]
        position_entity.sourcepositionid = item["sourcepositionid"]
        position_entity.status = item["status"]
        position_entity.branchid = item["branchid"]
        position_entity.sourceurl = item["sourceurl"]

        position = self.session.query(PositionInfo).filter(
            and_(PositionInfo.source == position_entity.source,
                 PositionInfo.sourcepositionid == position_entity.sourcepositionid
                 )).first()
        # logging.info(position.__dict__)
        if position:
            position_entity.positionID = position.positionID
            position_entity.updatedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            position_entity.positionID = str(uuid.uuid1())
            position_entity.createdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            position_entity.updatedate = position_entity.createdate
        self.session.merge(position_entity)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
