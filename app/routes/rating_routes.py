from flask import Blueprint, jsonify, request

rating_routes = Blueprint("rating_routes", __name__)

ratings = []

@rating_routes.route("/ratings", methods=["POST"])
def add_rating():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    rating = data.get("rating")

    if not user_id or not book_id or rating is None:
        return jsonify({"error": "user_id, book_id, and rating are required"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"error": "rating must be between 1 and 5"}), 400

    new_rating = {
        "user_id": user_id,
        "book_id": book_id,
        "rating": rating
    }

    ratings.append(new_rating)

    return jsonify({
        "message": "Rating added successfully",
        "rating": new_rating
    }), 201


@rating_routes.route("/books/<int:book_id>/rating", methods=["GET"])
def get_average_rating(book_id):
    book_ratings = [rating["rating"] for rating in ratings if rating["book_id"] == book_id]

    if not book_ratings:
        return jsonify({
            "book_id": book_id,
            "average_rating": None,
            "message": "No ratings yet"
        }), 200

    average = sum(book_ratings) / len(book_ratings)

    return jsonify({
        "book_id": book_id,
        "average_rating": round(average, 2)
    }), 200


@rating_routes.route("/ratings/<int:book_id>", methods=["PUT"])
def update_rating(book_id):
    data = request.get_json()

    user_id = data.get("user_id")
    new_rating = data.get("rating")

    if not user_id or new_rating is None:
        return jsonify({"error": "user_id and rating are required"}), 400

    if new_rating < 1 or new_rating > 5:
        return jsonify({"error": "rating must be between 1 and 5"}), 400

    for rating in ratings:
        if rating["book_id"] == book_id and rating["user_id"] == user_id:
            rating["rating"] = new_rating
            return jsonify({
                "message": "Rating updated successfully",
                "rating": rating
            }), 200

    return jsonify({"error": "Rating not found"}), 404