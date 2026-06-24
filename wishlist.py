from flask import Flask, jsonify, request

app = Flask(__name__)

wishlists = []
wishlist_items = []

books = [
    {"book_id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 14.99},
    {"book_id": 2, "title": "1984", "author": "George Orwell", "price": 12.50},
    {"book_id": 3, "title": "Dune", "author": "Frank Herbert", "price": 18.99}
]


@app.route("/wishlist", methods=["POST"])
def create_wishlist():
    data = request.get_json()

    user_id = data.get("user_id")
    wishlist_name = data.get("wishlist_name")

    if not user_id or not wishlist_name:
        return jsonify({"error": "user_id and wishlist_name are required"}), 400

    new_wishlist = {
        "wishlist_id": len(wishlists) + 1,
        "user_id": user_id,
        "wishlist_name": wishlist_name
    }

    wishlists.append(new_wishlist)

    return jsonify(new_wishlist), 201


@app.route("/wishlist/book", methods=["POST"])
def add_book_to_wishlist():
    data = request.get_json()

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if not wishlist_id or not book_id:
        return jsonify({"error": "wishlist_id and book_id are required"}), 400

    book_exists = any(book["book_id"] == book_id for book in books)

    if not book_exists:
        return jsonify({"error": "book not found"}), 404

    new_item = {
        "wishlist_item_id": len(wishlist_items) + 1,
        "wishlist_id": wishlist_id,
        "book_id": book_id
    }

    wishlist_items.append(new_item)

    return jsonify(new_item), 201


@app.route("/wishlist/book", methods=["DELETE"])
def remove_book_from_wishlist():
    data = request.get_json()

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if not wishlist_id or not book_id:
        return jsonify({"error": "wishlist_id and book_id are required"}), 400

    for item in wishlist_items:
        if item["wishlist_id"] == wishlist_id and item["book_id"] == book_id:
            wishlist_items.remove(item)
            return jsonify({
                "message": "book removed from wishlist",
                "wishlist_id": wishlist_id,
                "book_id": book_id
            }), 200

    return jsonify({"error": "book not found in wishlist"}), 404


@app.route("/wishlist/<int:wishlist_id>", methods=["GET"])
def get_books_in_wishlist(wishlist_id):
    wishlist_book_ids = [
        item["book_id"]
        for item in wishlist_items
        if item["wishlist_id"] == wishlist_id
    ]

    result = [
        book for book in books
        if book["book_id"] in wishlist_book_ids
    ]

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)