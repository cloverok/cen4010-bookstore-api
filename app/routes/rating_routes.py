from flask import Blueprint, jsonify, request

rating_routes = Blueprint("rating_routes", __name__)

ratings = []

@rating_routes.route("/ratings", methods=["POST"])
def add_rating():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    rating_value = data.get("rating")

    if user_id is None or book_id is None or rating_value is None:
        return jsonify({
            "error": "user_id, book_id, and rating are required"
        }), 400

    if rating_value < 1 or rating_value > 5:
        return jsonify({
            "error": "rating must be between 1 and 5"
        }), 400

    # Prevent the same user from rating the same book twice
    for existing_rating in ratings:
        if (
            existing_rating["user_id"] == user_id
            and existing_rating["book_id"] == book_id
        ):
            return jsonify({
                "error": "User has already rated this book. Use PUT to update the rating."
            }), 409

    new_rating = {
        "user_id": user_id,
        "book_id": book_id,
        "rating": rating_value
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

# Calculate the average rating for the requested book
    average = sum(book_ratings) / len(book_ratings)

    return jsonify({
    "book_id": book_id,
    "average_rating": round(average, 2),
    "total_ratings": len(book_ratings)
    }), 200


@rating_routes.route("/ratings/<int:book_id>", methods=["PUT"])
def update_rating(book_id):
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    new_rating = data.get("rating")

    if user_id is None or new_rating is None:
        return jsonify({
            "error": "user_id and rating are required"
        }), 400

    if new_rating < 1 or new_rating > 5:
        return jsonify({
            "error": "rating must be between 1 and 5"
        }), 400

    for rating in ratings:
        if rating["book_id"] == book_id and rating["user_id"] == user_id:
            rating["rating"] = new_rating

            return jsonify({
                "message": "Rating updated successfully",
                "rating": rating
            }), 200

    return jsonify({"error": "Rating not found"}), 404

@rating_routes.route("/ratings/<int:book_id>", methods=["DELETE"])
def delete_rating(book_id):
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    for rating in ratings:
        if rating["book_id"] == book_id and rating["user_id"] == user_id:
            ratings.remove(rating)

            return jsonify({
                "message": "Rating deleted successfully"
            }), 200

    return jsonify({"error": "Rating not found"}), 404