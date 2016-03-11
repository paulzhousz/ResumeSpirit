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
from models.positionresume import PositionResume
from items import ResumeItem, PositionItem


class ResumespiritPipeline(object):
    def open_spider(self, spider):
        self.session = config.db_session()

    def process_item(self, item, spider):
        # logging.info(item.__dict__)
        # 处理职位数据
        if isinstance(item, PositionItem):
            try:
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
            except Exception:
                logging.error(u"insert position data to database failed!")
        # 处理简历数据
        if isinstance(item, ResumeItem):
            resume_entity = ResumeInfo()
            try:
                resume_entity.cname = item["cname"]
                resume_entity.ename = item["ename"]
                resume_entity.sex = item["sex"]
                resume_entity.Residence = item["residence"]
                resume_entity.idtype = item["idtype"]
                resume_entity.idnumber = item["idnumber"]
                resume_entity.birthdate = item["birthdate"]
                resume_entity.marital = item["marital"]
                resume_entity.phonenumber = item["phonenumber"]
                resume_entity.mobile = item["mobile"]
                resume_entity.email = item["email"]
                resume_entity.qqnumber = item["qqnumber"]
                resume_entity.partisan = item["partisan"]
                resume_entity.hukou = item["hukou"]
                resume_entity.address = item["address"]
                resume_entity.degree = item["degree"]
                resume_entity.workingstart = item["workingstart"]
                resume_entity.currentsalary = item["currentsalary"]
                resume_entity.jobstatus = item["jobstatus"]
                resume_entity.overseaexp = item["overseaexp"]
                resume_entity.overseadesc = item["overseadesc"]
                resume_entity.avaliabletime = item["avaliabletime"]
                resume_entity.jobtime = item["jobtime"]
                resume_entity.expectindustry = item["expectindustry"]
                resume_entity.expectsalary = item["expectsalary"]
                resume_entity.category = item["category"]
                resume_entity.eduinfo = item["eduinfo"]
                resume_entity.traininginfo = item["traininginfo"]
                resume_entity.workexpinfo = item["workexpinfo"]
                resume_entity.projectexpinfo = item["projectexpinfo"]
                resume_entity.englishlevel = item["englishlevel"]
                resume_entity.japaneselevel = item["japaneselevel"]
                resume_entity.selfevaluation = item["selfevaluation"]
                resume_entity.skill = item["skill"]
                resume_entity.posttime = item["posttime"]
                resume_entity.source = item["source"]
                resume_entity.sourceresumeid = item["sourceresumeid"]
                resume_entity.sourceurl = item["sourceurl"]
                resume_entity.status = item["status"]

                resume = self.session.query(ResumeInfo).filter(
                    and_(ResumeInfo.source == resume_entity.source,
                         ResumeInfo.sourceurl == resume_entity.sourceurl
                         )).first()
                if resume:
                    resume_entity.resumeid = resume.resumeid
                    resume_entity.updatedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    resume_entity.resumeid = str(uuid.uuid1())
                    resume_entity.createdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    resume_entity.updatedate = resume_entity.createdate

                self.session.merge(resume_entity)
                self.session.commit()

                # 处理职位简历关联关系
                try:
                    sourcesite = item["source"]
                    positioncode = item["sourcepositionid"]
                    position = self.session.query(PositionInfo).filter(
                        and_(PositionInfo.source == sourcesite,
                             PositionInfo.sourcepositionid == positioncode
                             )).first()
                    if position:
                        relation = self.session.query(PositionResume).filter(
                            and_(PositionResume.positionid == position.positionID,
                                 PositionResume.resumeid == resume_entity.resumeid
                                 )).first()
                        if not relation:
                            relation_entity = PositionResume()
                            relation_entity.id = str(uuid.uuid1())
                            relation_entity.positionid = position.positionID
                            relation_entity.resumeid = resume_entity.resumeid
                            relation_entity.createdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            relation_entity.updatedate = relation_entity.createdate
                            self.session.add(relation_entity)
                            self.session.commit()
                    else:
                        logging.warning("Can't find position data:" + positioncode)
                except Exception:
                    raise Exception("insert position-resume relation data to database failed!")
            except Exception:
                logging.error(Exception.message)
        return item

    def close_spider(self, spider):
        self.session.close()
