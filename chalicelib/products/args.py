from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Products


class ProductsSchema(SQLAlchemySchema):
    class Meta:
        model = Products
        load_instance = True  # Optional: deserialize to model instances

    id = auto_field()
    name = auto_field()
    price = auto_field()
    unit_measure = auto_field()


