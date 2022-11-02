import tempfile

from boto3 import s3
from chalice import Chalice
from chalicelib.db import create_all_models, create_triggers
from chalicelib.products.router import product_routes
from chalicelib.sales.router import sales_routes
from chalicelib.unit_measure.router import unit_measure_routes

app = Chalice(app_name="products-api")
app.register_blueprint(product_routes)
app.register_blueprint(unit_measure_routes)
app.register_blueprint(sales_routes)
print("Starting")
create_all_models()
create_triggers()


@app.on_s3_event(
    "cdk-hnb659fds-assets-268904430734-us-east-1", events=["s3:ObjectCreated:Put"]
)
def resize_image(event):

    with tempfile.NamedTemporaryFile("w") as f:
        s3.download_file(event.bucket, event.key, f.name)
        print(f.name)

