from flask import Flask, jsonify, request

app = Flask(__name__)

ratings = []
comments = []

@app.route("/")
def home():
    return jsonify({
        "message": "CEN4010 Bookstore API is running",
        "status": "success"
    })

@app.route("/ratings", methods=["POST"])
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

@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    comment = data.get("comment")

    if not user_id or not book_id or not comment:
        return jsonify({"error": "user_id, book_id, and comment are required"}), 400

    new_comment = {
        "user_id": user_id,
        "book_id": book_id,
        "comment": comment
    }

    comments.append(new_comment)

    return jsonify({
        "message": "Comment added successfully",
        "comment": new_comment
    }), 201

@app.route("/books/<int:book_id>/comments", methods=["GET"])
def get_comments(book_id):
    book_comments = [comment for comment in comments if comment["book_id"] == book_id]
    return jsonify(book_comments), 200

@app.route("/books/<int:book_id>/rating", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)