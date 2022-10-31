import datetime

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
    DateTime as SdateTime,
    TypeDecorator,
)
from sqlalchemy.orm import declarative_base, relationship
from chalicelib.db import Base
import pytz


class UnitMeasure(Base):
    __tablename__ = "tblUnitMeasure"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    product = relationship("Products", back_populates="unit_measure", lazy="joined")

    def __init__(self, name):
        self.name = name


class Products(Base):
    __tablename__ = "tblProducts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0)
    unit_measure_id = Column(Integer, ForeignKey("tblUnitMeasure.id"), nullable=False)
    stock = Column(Integer, server_default="0", default=0)
    sales_item = relationship("SalesItem", back_populates="products", lazy="joined")
    unit_measure = relationship("UnitMeasure", back_populates="product", lazy="joined")

    def __init__(self, name, price, unit_measure_id, stock):
        self.name = name
        self.price = round(price, 2)
        self.unit_measure_id = unit_measure_id
        self.stock = stock


class MexicoDateTime(TypeDecorator):
    impl = SdateTime

    def process_bind_param(self, value, engine):
        return value

    def process_result_value(self, value, engine):
        return value.replace(tzinfo=pytz.timezone("Asia/Tokyo")).astimezone(
            pytz.timezone("America/Mexico_City")
        )


class Sales(Base):
    __tablename__ = "tblSales"

    id = Column(Integer, primary_key=True)
    sale_amount = Column(
        DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0
    )
    time_created = sqlalchemy.Column(MexicoDateTime, default=datetime.datetime.now)
    sales_items = relationship("SalesItem", lazy="joined")

    def __init__(self, name):
        self.name = name


class SalesItem(Base):
    __tablename__ = "tblSalesItem"

    id = Column(Integer, primary_key=True)
    sale_amount = Column(
        DECIMAL(precision=100, scale=2), server_default="0.0", default=0.0
    )
    quantity_sold = Column(Integer, server_default="0", default=0)
    sales_id = Column(Integer, ForeignKey("tblSales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tblProducts.id"), nullable=False)
    products = relationship("Products", back_populates="sales_item", lazy="joined")
