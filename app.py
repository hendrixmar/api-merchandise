from chalice import Chalice
import requests

app = Chalice(app_name='products-api')

@app.route('/')
def index():
    return {'hello': 'world'}


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
        Item = {
            'id': book_as_json['id'],
            "title": book_as_json['title'],
            "author": book_as_json['author']
        }
        return {"id": book_as_json['id'], "title": book_as_json['title'], "author": book_as_json['author']}
    except Exception as e:
        return {'message': str(e)}


# PUT endpoint to update a book item based on the given ID

@app.route('/book/{id}', methods=['PUT'])
def update_book(id):
    book_as_json = app.current_request.json_body
    try:
        Item = {
            "id": book_as_json['id'],
            "title": book_as_json['title'],
        }
        return {'message': 'ok - UPDATED', 'status': 201}
    except Exception as e:
        return {'message': str(e)}


# DELETE endpoint to delete a particular book based on the given ID

@app.route('/book/{id}', methods=['DELETE'])
def delete_book(id):
    book_as_json = app.current_request.json_body
    try:
        Item = {
            "id": book_as_json['id'],
            "author": book_as_json['author']
        }
        return {'message': 'ok - DELETED', 'status': 201}
    except Exception as e:
        return {'message': str(e)}