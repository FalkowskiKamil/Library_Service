from collections import namedtuple
from flask import Flask, request, redirect, render_template, url_for, jsonify, abort, make_response
from forms import BookForm
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


User = namedtuple("User", field_names=["email", "password"])
user = User(email="john@black.com", password="black")


@app.route("/api/library/",methods=["GET"])
def books_list_api():
    return jsonify(books.all())

@app.route("/api/library/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})

@app.route("/api/library/", methods=["POST"])
def create_book():
    if not request.json or not 'title' or not 'author' in request.json:
        abort(404)
    book = {
        'id': books.all()[-0]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'description':request.json.get('description', ""),
        'year':request.json.get('year', ""),
        'category': request.json.get('category', "")
    }
    books.create(book)
    return jsonify({'book': book}), 201

@app.route('/api/library/<int:book_id>', methods= ["DELETE"])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route('/api/library/<int:book_id>', methods = ["PUT"])
def update_book(book_id):
    book=books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'year' in data and not isinstance(data.get('year'), str),
        'category' in data and not isinstance(data.get('category'), str)
    ]):
        abort(404)
    book = {
        'id': data.get('id', book['id']),
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'description': data.get('description', book['description']),
        'year': data.get('year', book['year']),
        'category': data.get('category', book['category']),
    }
    books.update(book_id, book)
    return jsonify({'book':book})

@app.route("/library/", methods=["GET", "POST"])
def books_list():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("books_list"))

    return render_template("books.html", form=form, books=books.all(), error=error)

@app.route("/library/add", methods=["POST"])
def add_book():
    form =BookForm()
    error = ""
    return render_template("add.html",form=form, error=error )

@app.route("/library/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get_2(book_id - 1)
    form = BookForm(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            books.update_2(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=False)