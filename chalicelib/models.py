import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DECIMAL,
    CheckConstraint,
    DDL,
    event,
)
from sqlalchemy.orm import declarative_base, relationship
from chalicelib.db import Base


class UnitMeasure(Base):
    __tablename__ = "tblUnitMeasure"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Products(Base):
    __tablename__ = "tblProducts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0)
    unit_measure_id = Column(Integer, ForeignKey("tblUnitMeasure.id"), nullable=False)
    stock = Column(Integer, server_default="0", default=0)

    def __init__(self, name, price, unit_measure_id, stock):
        self.name = name
        self.price = round(price, 2)
        self.unit_measure_id = unit_measure_id
        self.stock = stock


class Sales(Base):
    __tablename__ = "tblSales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_amount = Column(DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0)
    time_created = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now()
    )
    sales_items = relationship("SalesItem")

    def __init__(self, name):
        self.name = name


class SalesItem(Base):
    __tablename__ = "tblSalesItem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_amount = Column(DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0)
    quantity_sold = Column(Integer, server_default="0", default=0)
    sales_id = Column(Integer, ForeignKey("tblSales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tblProducts.id"), nullable=False)

    def __init__(self, name):
        self.name = name
