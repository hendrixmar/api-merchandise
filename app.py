from chalice import Chalice
from chalicelib.db import create_all_models, create_triggers
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from chalicelib.products.routes import product_routes
from chalicelib.sales.routes import sales_routes
from chalicelib.unit_measure.routes import unit_measure_routes

app = Chalice(app_name="products-api")
app.register_blueprint(product_routes)
app.register_blueprint(unit_measure_routes)
app.register_blueprint(sales_routes)
print("Starting")
create_all_models()
create_triggers()
