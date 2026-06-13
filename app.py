from flask import Flask, jsonify, request

app = Flask(__name__)

books = []
authors = []

@app.route("/")
def home():
    return "Bookstore API is running."

@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    author = {
        "author_id": len(authors) + 1,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "biography": data.get("biography"),
        "publisher": data.get("publisher")
    }
    authors.append(author)
    return jsonify({"message": "Author created successfully", "author": author}), 201

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    books.append(data)
    return jsonify({"message": "Book created successfully", "book": data}), 201

@app.route("/books/<isbn>", methods=["GET"])
def get_book_by_isbn(isbn):
    for book in books:
        if book["isbn"] == isbn:
            return jsonify(book), 200
    return jsonify({"message": "Book not found"}), 404

@app.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):
    author_books = [book for book in books if book.get("author_id") == author_id]
    return jsonify(author_books), 200

if __name__ == "__main__":
    app.run(debug=True)