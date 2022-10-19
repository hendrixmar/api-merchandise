from chalice import Chalice
import os
from datetime import date
import requests
from chalicelib.products.routes import extra_routes
from sqlalchemy import create_engine
from chalicelib.db import Movie
from sqlalchemy.orm import sessionmaker, declarative_base


if os.getenv("GITHUB_ACTION"):
    config = {key: os.getenv(key) for key in ['DB_USER','DB_PASS', 'DB_HOST', 'DB_NAME']}
else:
    from dotenv import load_dotenv, dotenv_values
    load_dotenv()  # take environment variables from .env.
    config = dict(dotenv_values(".env"))

print(config)
app = Chalice(app_name='products-api')
DATABASE_URL = f"postgresql+psycopg2://{config.get('DB_USER')}:{config.get('DB_PASS')}@{config.get('DB_HOST')}/{config.get('DB_NAME')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
# create a Session
app.register_blueprint(extra_routes)


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
