from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///D:\\talent_pool_db\\Talent_Sourcing.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

session.close()

class TalentPool(Base):
    __tablename__ = 'Talent_Pool'
    talent_id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    linkedin_link = Column(String(250))
    position = Column(String(250))

    @classmethod
    def instert_talent_pool(cls, talent):
        new_talent = TalentPool(fullname=talent['fullname'], linkedin_link=talent['linkedin_path'], position=talent['position'])
        session.add(new_talent)
        session.commit()
        print("Inserted")

    @classmethod
    def select_talent_pool(cls):
        talent_pool_data = session.query(TalentPool).all()
        return talent_pool_data

class Experience(Base):
    __tablename__ = 'Expericence'
    experience_id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(100), nullable=False)
    month = Column(Integer)
    position = Column(String(250))
    # talent_id = relationship('TalentPool', foreign_keys='TalentPool.talent_id')

    # @classmethod
    # def instert_experience(talent_experience):
    #     new_talent = TalentPool(company=talent_experience['company'], month=talent_experience['month'], position=talent_experience[''], talent_id=talent_experience[''])
    #     session.add(new_talent)
    #     session.commit()


class SkillsAndLanguages(Base):
    __tablename__ = "SkillsAndLanguages"
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill = Column(String(250), nullable=False)
    rating = Column(Integer)
    # talent_id = relationship('TalentPool', foreign_keys='TalentPool.talent_id')

    # @classmethod
    # def instert_experience(talent_skills):
    #     new_talent = TalentPool(skill=talent_skills['company'], rating=talent_skills[''])
    #     session.add(new_talent)
    #     session.commit()


Base.metadata.create_all(engine)

