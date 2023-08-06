from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

from mo9mo9db.base_mixin import DBBaseMixin
from mo9mo9db.dbsession import get_db_engine

engine = get_db_engine()
Base = declarative_base()


class Studytimelogs(DBBaseMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    study_dt = Column(DateTime, unique=False)
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=False)
    voice_id = Column(String(20), unique=False)
    access = Column(String(10), unique=False)
    studytime_min = Column(Integer, unique=False)
    studytag_no = Column(String(10), unique=False)
    excluded_record = Column(Boolean)

    def __init__(self,
                 study_dt=None,
                 guild_id=None,
                 member_id=None,
                 voice_id=None,
                 access=None,
                 studytime_min=None,
                 studytag_no=None,
                 excluded_record=None):
        self.study_dt = study_dt
        self.guild_id = guild_id
        self.member_id = member_id
        self.access = access
        self.voice_id = voice_id
        self.studytime_min = studytime_min
        self.studytag_no = studytag_no
        self.excluded_record = excluded_record


class Studymembers(DBBaseMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=True)
    member_name = Column(String(50))
    joined_dt = Column(DateTime, unique=False)
    enrollment = Column(Boolean)

    def __init__(self,
                 guild_id=None,
                 member_id=None,
                 member_name=None,
                 joined_dt=None,
                 enrollment=None):
        self.guild_id = guild_id
        self.member_id = member_id
        self.member_name = member_name
        self.joined_dt = joined_dt
        self.enrollment = enrollment


class Selfintroduction(DBBaseMixin, Base):
    __table_args__ = ({"mysql_charset": "utf8mb4",
                       "mysql_collate": "utf8mb4_bin",
                       "mysql_row_format": "DYNAMIC"})
    guild_id = Column(String(20), primary_key=True)
    member_id = Column(String(20), primary_key=True)
    nickname = Column(String(50))
    gender = Column(String(20))
    twitter_id = Column(String(50))
    specialty = Column(Text)
    before_study = Column(Text)
    after_study = Column(Text)
    sendmsg_id = Column(String(20))
    mod_column = Column(String(20))

    def __init__(self,
                 guild_id=None,
                 member_id=None,
                 nickname=None,
                 gender=None,
                 twitter_id=None,
                 specialty=None,
                 before_study=None,
                 after_study=None,
                 sendmsg_id=None,
                 mod_column=None,
                 ):

        self.guild_id = guild_id
        self.member_id = member_id
        self.nickname = nickname
        self.gender = gender
        self.twitter_id = twitter_id
        self.specialty = specialty
        self.before_study = before_study
        self.after_study = after_study
        self.sendmsg_id = sendmsg_id
        self.mod_colmun = mod_column


Base.metadata.create_all(bind=engine)
