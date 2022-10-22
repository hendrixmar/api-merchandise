from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UnitMeasure(Base):
    __tablename__ = 'tblUnitMeasure'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __iter__(self):
        return ((column, str(getattr(self, column))) for column in self.__table__.c.keys())


print("AQUI-measure")
