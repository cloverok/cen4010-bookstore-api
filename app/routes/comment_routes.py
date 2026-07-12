from flask import Blueprint, jsonify, request

comment_routes = Blueprint("comment_routes", __name__)

comments = []

@comment_routes.route("/comments", methods=["POST"])
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


@comment_routes.route("/books/<int:book_id>/comments", methods=["GET"])
def get_comments(book_id):
    book_comments = [comment for comment in comments if comment["book_id"] == book_id]
    return jsonify(book_comments), 200


@comment_routes.route("/comments/<int:book_id>", methods=["DELETE"])
def delete_comment(book_id):
    data = request.get_json()

    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    for comment in comments:
        if comment["book_id"] == book_id and comment["user_id"] == user_id:
            comments.remove(comment)
            return jsonify({
                "message": "Comment deleted successfully"
            }), 200

@comment_routes.route("/comments/<int:book_id>", methods=["PUT"])
def update_comment(book_id):
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    new_comment = data.get("comment")

    if user_id is None or not new_comment:
        return jsonify({
            "error": "user_id and comment are required"
        }), 400

    for comment in comments:
        if comment["book_id"] == book_id and comment["user_id"] == user_id:
            comment["comment"] = new_comment

            return jsonify({
                "message": "Comment updated successfully",
                "comment": comment
            }), 200

    return jsonify({"error": "Comment not found"}), 404 