from flask import Blueprint, jsonify, request

wishlist_bp = Blueprint("wishlist", __name__)

wishlists = []
wishlist_items = []

books = [
    {
        "book_id": 1,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "price": 14.99,
    },
    {
        "book_id": 2,
        "title": "1984",
        "author": "George Orwell",
        "price": 12.50,
    },
    {
        "book_id": 3,
        "title": "Dune",
        "author": "Frank Herbert",
        "price": 18.99,
    },
]


def find_wishlist(wishlist_id):
    """Return the wishlist with the given ID, or None if it does not exist."""
    return next(
        (
            wishlist
            for wishlist in wishlists
            if wishlist["wishlist_id"] == wishlist_id
        ),
        None,
    )


def find_book(book_id):
    """Return the book with the given ID, or None if it does not exist."""
    return next(
        (book for book in books if book["book_id"] == book_id),
        None,
    )


@wishlist_bp.route("/wishlist", methods=["POST"])
def create_wishlist():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "A JSON request body is required."}), 400

    user_id = data.get("user_id")
    wishlist_name = data.get("wishlist_name")

    if user_id is None or wishlist_name is None:
        return jsonify(
            {"error": "user_id and wishlist_name are required."}
        ), 400

    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(
            {"error": "user_id must be a positive integer."}
        ), 400

    if not isinstance(wishlist_name, str) or not wishlist_name.strip():
        return jsonify(
            {"error": "wishlist_name must be a non-empty string."}
        ), 400

    new_wishlist = {
        "wishlist_id": len(wishlists) + 1,
        "user_id": user_id,
        "wishlist_name": wishlist_name.strip(),
    }

    wishlists.append(new_wishlist)

    return jsonify(new_wishlist), 201


@wishlist_bp.route("/wishlist/book", methods=["POST"])
def add_book_to_wishlist():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "A JSON request body is required."}), 400

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if wishlist_id is None or book_id is None:
        return jsonify(
            {"error": "wishlist_id and book_id are required."}
        ), 400

    if not isinstance(wishlist_id, int) or wishlist_id <= 0:
        return jsonify(
            {"error": "wishlist_id must be a positive integer."}
        ), 400

    if not isinstance(book_id, int) or book_id <= 0:
        return jsonify(
            {"error": "book_id must be a positive integer."}
        ), 400

    if find_wishlist(wishlist_id) is None:
        return jsonify({"error": "Wishlist not found."}), 404

    if find_book(book_id) is None:
        return jsonify({"error": "Book not found."}), 404

    duplicate_item = next(
        (
            item
            for item in wishlist_items
            if item["wishlist_id"] == wishlist_id
            and item["book_id"] == book_id
        ),
        None,
    )

    if duplicate_item is not None:
        return jsonify(
            {"error": "Book already exists in this wishlist."}
        ), 409

    new_item = {
        "wishlist_item_id": len(wishlist_items) + 1,
        "wishlist_id": wishlist_id,
        "book_id": book_id,
    }

    wishlist_items.append(new_item)

    return jsonify(new_item), 201


@wishlist_bp.route("/wishlist/book", methods=["DELETE"])
def remove_book_from_wishlist():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "A JSON request body is required."}), 400

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if wishlist_id is None or book_id is None:
        return jsonify(
            {"error": "wishlist_id and book_id are required."}
        ), 400

    if not isinstance(wishlist_id, int) or wishlist_id <= 0:
        return jsonify(
            {"error": "wishlist_id must be a positive integer."}
        ), 400

    if not isinstance(book_id, int) or book_id <= 0:
        return jsonify(
            {"error": "book_id must be a positive integer."}
        ), 400

    if find_wishlist(wishlist_id) is None:
        return jsonify({"error": "Wishlist not found."}), 404

    if find_book(book_id) is None:
        return jsonify({"error": "Book not found."}), 404

    item_to_remove = next(
        (
            item
            for item in wishlist_items
            if item["wishlist_id"] == wishlist_id
            and item["book_id"] == book_id
        ),
        None,
    )

    if item_to_remove is None:
        return jsonify(
            {"error": "Book not found in this wishlist."}
        ), 404

    wishlist_items.remove(item_to_remove)

    return jsonify(
        {
            "message": "Book removed from wishlist.",
            "wishlist_id": wishlist_id,
            "book_id": book_id,
        }
    ), 200


@wishlist_bp.route("/wishlist/<int:wishlist_id>", methods=["GET"])
def get_books_in_wishlist(wishlist_id):
    if find_wishlist(wishlist_id) is None:
        return jsonify({"error": "Wishlist not found."}), 404

    wishlist_book_ids = [
        item["book_id"]
        for item in wishlist_items
        if item["wishlist_id"] == wishlist_id
    ]

    result = [
        book
        for book in books
        if book["book_id"] in wishlist_book_ids
    ]

    return jsonify(result), 200