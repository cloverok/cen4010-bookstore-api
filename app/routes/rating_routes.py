from flask import Blueprint, jsonify, request
from pymysql.err import IntegrityError

from app.database.db import get_db_connection


rating_routes = Blueprint("rating_routes", __name__)


def validate_rating(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 5


@rating_routes.route("/ratings", methods=["POST"])
def add_rating():
    data = request.get_json(silent=True) or {}
    uid = data.get("uid")
    book_id = data.get("book_id")
    rating_value = data.get("rating")

    if uid is None or book_id is None or rating_value is None:
        return jsonify({"error": "uid, book_id, and rating are required"}), 400

    if not validate_rating(rating_value):
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ratings (uid, book_id, rating)
                VALUES (%s, %s, %s)
                """,
                (uid, book_id, rating_value),
            )
            rating_id = cursor.lastrowid

        connection.commit()
        return jsonify({
            "message": "Rating added successfully",
            "rating": {
                "rating_id": rating_id,
                "uid": uid,
                "book_id": book_id,
                "rating": rating_value,
            },
        }), 201

    except IntegrityError as error:
        connection.rollback()

        if error.args and error.args[0] == 1062:
            return jsonify({
                "error": "User has already rated this book. Use PUT to update the rating."
            }), 409

        if error.args and error.args[0] == 1452:
            return jsonify({"error": "uid or book_id does not exist"}), 404

        return jsonify({"error": "Unable to add rating"}), 500

    finally:
        connection.close()


@rating_routes.route("/books/<int:book_id>/rating", methods=["GET"])
def get_average_rating(book_id):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(rating) AS average_rating, COUNT(*) AS total_ratings
                FROM ratings
                WHERE book_id = %s
                """,
                (book_id,),
            )
            result = cursor.fetchone()

        total_ratings = result["total_ratings"]
        if total_ratings == 0:
            return jsonify({
                "book_id": book_id,
                "average_rating": None,
                "total_ratings": 0,
                "message": "No ratings yet",
            }), 200

        return jsonify({
            "book_id": book_id,
            "average_rating": round(float(result["average_rating"]), 2),
            "total_ratings": total_ratings,
        }), 200

    finally:
        connection.close()


@rating_routes.route("/ratings/<int:book_id>", methods=["PUT"])
def update_rating(book_id):
    data = request.get_json(silent=True) or {}
    uid = data.get("uid")
    rating_value = data.get("rating")

    if uid is None or rating_value is None:
        return jsonify({"error": "uid and rating are required"}), 400

    if not validate_rating(rating_value):
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ratings
                SET rating = %s
                WHERE uid = %s AND book_id = %s
                """,
                (rating_value, uid, book_id),
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return jsonify({"error": "Rating not found"}), 404

        connection.commit()
        return jsonify({
            "message": "Rating updated successfully",
            "rating": {
                "uid": uid,
                "book_id": book_id,
                "rating": rating_value,
            },
        }), 200

    finally:
        connection.close()


@rating_routes.route("/ratings/<int:book_id>", methods=["DELETE"])
def delete_rating(book_id):
    data = request.get_json(silent=True) or {}
    uid = data.get("uid")

    if uid is None:
        return jsonify({"error": "uid is required"}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM ratings
                WHERE uid = %s AND book_id = %s
                """,
                (uid, book_id),
            )

            if cursor.rowcount == 0:
                connection.rollback()
                return jsonify({"error": "Rating not found"}), 404

        connection.commit()
        return jsonify({"message": "Rating deleted successfully"}), 200

    finally:
        connection.close()
