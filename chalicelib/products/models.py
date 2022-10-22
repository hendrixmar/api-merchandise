from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Products(Base):
    __tablename__ = 'tblProducts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(DECIMAL(precision=1000, scale=2))
    unit_measure = Column(Integer)

    def __init__(self, name, price):
        self.name = name
        self.price = round(price, 2)
        self.unit_measure = 420

    def __iter__(self):
        return ((column, str(getattr(self, column))) for column in self.__table__.c.keys())

print("AQUI-products")