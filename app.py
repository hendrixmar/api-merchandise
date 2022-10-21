from chalice import Chalice
import os
from datetime import date
import requests
from chalicelib.products.routes import product_routes
from chalicelib.db import Session, Base, engine
from chalicelib.models import Movie
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

app = Chalice(app_name='products-api')
app.register_blueprint(product_routes)
Base.metadata.create_all(engine)


