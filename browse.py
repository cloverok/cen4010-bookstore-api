# routes/browse.py

from flask import Blueprint, jsonify
from models.book import Book

browse_bp = Blueprint(
    "browse",
    __name__,
    url_prefix="/books"
)

@browse_bp.route("/genre/<genre>", methods=["GET"])
def get_books_by_genre(genre):

    books = Book.query.filter_by(
        genre=genre
    ).all()

    return jsonify(
        [book.to_dict() for book in books]
    )