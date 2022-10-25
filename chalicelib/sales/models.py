import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from chalicelib.db import Base


class Sales(Base):
    __tablename__ = "tblSales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_amount = Column(Integer, unique=True, nullable=False)
    time_created = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now()
    )
    sales_items = relationship("SalesItem")

    def __init__(self, name):
        self.name = name


class SalesItem(Base):
    __tablename__ = "tblSalesItem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_amount = Column(Integer, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    time_created = Column(
        sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now()
    )
    sales_items = relationship("Sales")
    product_id = Column(Integer, ForeignKey("tblProducts.id"), nullable=False)

    def __init__(self, name):
        self.name = name

print("3")