drop index T_BranchSource_PK;

drop table T_BranchSource;

drop index T_PositionInfo_PK;

drop table T_PositionInfo;

drop index T_PositionResume_PK;

drop table T_PositionResume;

drop index T_ResumeInfo_PK;

drop table T_ResumeInfo;

drop index T_SourceSiteInfo_PK;

drop table T_SourceSiteInfo;

drop index T_branchInfo_PK;

drop table T_branchInfo;

drop index T_userInfo_PK;

drop table T_userInfo;

create table T_BranchSource (
BranchSourceID       VARCHAR(50)                    not null,
BranchID             VARCHAR(50),
SourceID             VARCHAR(50),
CompanyName          VARCHAR(50),
Username             VARCHAR(50),
PasswordSet          VARCHAR(100),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (BranchSourceID)
);

create unique index T_BranchSource_PK on T_BranchSource (
BranchSourceID ASC
);

create table T_PositionInfo (
PositionID           VARCHAR(50)                    not null,
PositionName         VARCHAR(100)                   not null,
HiringNumber         INTEGER,
Location             VARCHAR(50),
WorkingTime          VARCHAR(20),
Degree               VARCHAR(20),
Sex                  VARCHAR(10),
Language             VARCHAR(20),
LanguageLevel        VARCHAR(10),
AgeFrom              INTEGER,
AgeTo                INTEGER,
Experience           INTEGER,
Category             VARCHAR(100),
Major                VARCHAR(100),
Salary               VARCHAR(100),
PositionDesc         VARCHAR(2000),
EndDate              VARCHAR(20),
Source               VARCHAR(20),
sourcepositionID     VARCHAR(50),
Status               VARCHAR(10),
BranchID             VARCHAR(50),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (PositionID)
);

create unique index T_PositionInfo_PK on T_PositionInfo (
PositionID ASC
);

create table T_PositionResume (
ID                   VARCHAR(50)                    not null,
PositionID           VARCHAR(50),
ResumeID             VARCHAR(50),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (ID)
);

create unique index T_PositionResume_PK on T_PositionResume (
ID ASC
);

create table T_ResumeInfo (
resumeID             VARCHAR(50)                    not null,
cname                VARCHAR(20),
ename                VARCHAR(20),
sex                  VARCHAR(10),
IDtype               VARCHAR(20),
IDNumber             VARCHAR(50),
birthdate            VARCHAR(20),
marital              VARCHAR(10),
phoneNumber          VARCHAR(20),
mobile               VARCHAR(20),
email                VARCHAR(50),
qqNumber             VARCHAR(50),
partisan             VARCHAR(100),
hukou                VARCHAR(100),
address              VARCHAR(100),
degree               VARCHAR(50),
currentSalary        VARCHAR(50),
jobStatus            VARCHAR(50),
overseaExp           VARCHAR(10),
avaliableTime        VARCHAR(20),
jobTime              VARCHAR(10),
expectIndustry       VARCHAR(100),
expectSalary         VARCHAR(100),
category             VARCHAR(100),
EnglishLevel         VARCHAR(100),
selfEvaluation       VARCHAR(500),
skill                VARCHAR(500),
positionID           VARCHAR(50),
postTime             VARCHAR(30),
Source               VARCHAR(20),
sourceresumeID       VARCHAR(50),
sourcepositionID     VARCHAR(50),
Status               VARCHAR(10),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (resumeID)
);

create unique index T_ResumeInfo_PK on T_ResumeInfo (
resumeID ASC
);

create table T_SourceSiteInfo (
SourceID             VARCHAR(50)                    not null,
Code                 VARCHAR(20)                    not null,
"Desc"               VARCHAR(50),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (SourceID)
);

create unique index T_SourceSiteInfo_PK on T_SourceSiteInfo (
SourceID ASC
);

create table T_branchInfo (
BranchID             VARCHAR(50)                    not null,
cname                VARCHAR(100),
ename                VARCHAR(100),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (BranchID)
);

create unique index T_branchInfo_PK on T_branchInfo (
BranchID ASC
);

create table T_userInfo (
UserID               VARCHAR(50)                    not null,
LoginName            VARCHAR(20),
Username             VARCHAR(20),
PasswordSet          VARCHAR(100),
BranchID             VARCHAR(50),
IsAdmin              VARCHAR(10),
IsEnabled            VARCHAR(10),
CreateDate           VARCHAR(30),
UpdateDate           VARCHAR(30),
primary key (UserID)
);

create unique index T_userInfo_PK on T_userInfo (
UserID ASC
);

