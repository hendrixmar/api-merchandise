from chalice import Chalice
import os
from datetime import date
import requests
from chalicelib.products.routes import product_routes
from chalicelib.db import Session, Base, engine
from chalicelib.db import Movie
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
    # 3 - create a new session
    return {"madres": "Cabeshon"}


@app.route('/post')
def get_post():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.ok:
        return response.json()
    else:
        return None


@app.route('/book', methods=['POST'])
def create_book():
    book_as_json = app.current_request.json_body
    try:
        item = {
            "id": id,
            "author": book_as_json['author']
        }
        return {'message': item, 'status': 201}
    except Exception as e:
        return {'message': str(e)}


# PUT endpoint to update a book item based on the given ID

@app.route('/book/{id}', methods=['PUT'])
def update_book(id):
    book_as_json = app.current_request.json_body
    try:
        item = {
            "id": id,
            "author": book_as_json['author']
        }
        return {'message': item, 'status': 201}
    except Exception as e:
        return {'message': str(e)}


# DELETE endpoint to delete a particular book based on the given ID

@app.route('/book/{id}', methods=['DELETE'])
def delete_book(id):
    book_as_json = app.current_request.json_body
    try:
        item = {
            "id": id,
            "author": book_as_json['author']
        }
        return {'message': item, 'status': 201}
    except Exception as e:
        return {'message': str(e)}
