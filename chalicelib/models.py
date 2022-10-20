from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date
from chalicelib.db import Base

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def __iter__(self):
        return ((column, str(getattr(self, column))) for column in self.__table__.c.keys())


# create a Session
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __iter__(self):
        return ((column, str(getattr(self, column))) for column in self.__table__.c.keys())

