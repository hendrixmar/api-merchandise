from sqlalchemy import Column, Integer, String, Float, Boolean, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
