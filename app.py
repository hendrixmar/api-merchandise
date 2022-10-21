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

@app.route('/')
def index():
    with Session() as session:
        bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
        furious_7 = Movie("Furious 7", date(2015, 4, 2))
        pain_and_gain = Movie("Pain & Gain", date(2013, 8, 23))

        session.add(bourne_identity)
        session.add(furious_7)
        session.add(pain_and_gain)
        session.commit()
        temp = (dict(row) for row in session.query(Movie).all())
    # 3 - create a new session
    return [os.getenv("WE"), len(list(temp))]




