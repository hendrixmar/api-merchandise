from chalice import Chalice
import os
from datetime import date
import requests
from chalicelib.products.routes import product_routes
from chalicelib.db import engine, create_all_models, create_triggers

from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

from chalicelib.unit_measure.routes import unit_measure_routes

app = Chalice(app_name="products-api")
app.register_blueprint(product_routes)
app.register_blueprint(unit_measure_routes)
print("Aqui")
create_all_models()
create_triggers()
