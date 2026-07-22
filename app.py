from flask import Flask, jsonify, request

app = Flask(__name__)

books = []
authors = []


@app.route("/")
def home():
    return "Bookstore API is running."


@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Missing author data"}), 400

    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"message": "First name and last name are required"}), 400

    author = {
        "author_id": len(authors) + 1,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "biography": data.get("biography"),
        "publisher": data.get("publisher")
    }

    authors.append(author)

    return jsonify({
        "message": "Author created successfully",
        "author": author
    }), 201


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Missing book data"}), 400

    required_fields = [
        "isbn",
        "name",
        "description",
        "price",
        "author_id",
        "genre",
        "publisher",
        "year_published",
        "copies_sold"
    ]

    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"message": field + " is required"}), 400

    for book in books:
        if book["isbn"] == data["isbn"]:
            return jsonify({
                "message": "Book with this ISBN already exists"
            }), 400

    books.append(data)

    return jsonify({
        "message": "Book created successfully",
        "book": data
    }), 201


@app.route("/books/<isbn>", methods=["GET"])
def get_book_by_isbn(isbn):
    for book in books:
        if book["isbn"] == isbn:
            return jsonify(book), 200

    return jsonify({"message": "Book not found"}), 404


@app.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):

    author_exists = any(
        author["author_id"] == author_id
        for author in authors
    )

    if not author_exists:
        return jsonify({"message": "Author not found"}), 404

    author_books = [
        book
        for book in books
        if book.get("author_id") == author_id
    ]

    if not author_books:
        return jsonify({
            "message": "No books found for this author"
        }), 404

    return jsonify(author_books), 200


if __name__ == "__main__":
    app.run(debug=True)