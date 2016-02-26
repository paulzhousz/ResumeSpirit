drop index T_PositionInfo_PK;

drop table T_PositionInfo;

drop index T_ResumeInfo_PK;

drop table T_ResumeInfo;

create table T_PositionInfo (
positionid           VARCHAR(50)                    not null,
positionname         VARCHAR(100)                   not null,
hiringnumber         INTEGER,
location             VARCHAR(50),
workingtime          VARCHAR(20),
degree               VARCHAR(20),
sex                  VARCHAR(10),
language             VARCHAR(20),
languagelevel        VARCHAR(10),
agefrom              INTEGER,
ageto                INTEGER,
experience           INTEGER,
category             VARCHAR(100),
major                VARCHAR(100),
salary               VARCHAR(100),
positiondesc         VARCHAR(2000),
enddate              VARCHAR(20),
source               VARCHAR(20),
sourcepositionid     VARCHAR(50),
status               VARCHAR(10),
createdate           VARCHAR(30),
updatedate           VARCHAR(30),
primary key (positionid)
);

create unique index T_PositionInfo_PK on T_PositionInfo (
positionid ASC
);

create table T_ResumeInfo (
resumeid             VARCHAR(50)                    not null,
cname                VARCHAR(20),
ename                VARCHAR(20),
sex                  VARCHAR(10),
idtype               VARCHAR(20),
idnumber             VARCHAR(50),
birthdate            VARCHAR(20),
marital              VARCHAR(10),
phonenumber          VARCHAR(20),
mobile               VARCHAR(20),
email                VARCHAR(50),
qqnumber             VARCHAR(50),
partisan             VARCHAR(100),
hukou                VARCHAR(100),
address              VARCHAR(100),
degree               VARCHAR(50),
currentsalary        VARCHAR(50),
jobstatus            VARCHAR(50),
overseaexp           VARCHAR(10),
avaliabletime        VARCHAR(20),
jobtime              VARCHAR(10),
expectindustry       VARCHAR(100),
expectsalary         VARCHAR(100),
category             VARCHAR(100),
englishlevel         VARCHAR(100),
selfevaluation       VARCHAR(500),
skill                VARCHAR(500),
positionid           VARCHAR(50),
posttime             VARCHAR(30),
source               VARCHAR(20),
sourcepositionid     VARCHAR(50),
status               VARCHAR(10),
createdate           VARCHAR(30),
updatedate           VARCHAR(30),
primary key (resumeid)
);

create unique index T_ResumeInfo_PK on T_ResumeInfo (
resumeid ASC
);

