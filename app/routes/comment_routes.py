from flask import Blueprint, jsonify, request
from app.database.db import get_db_connection

comment_routes = Blueprint("comment_routes", __name__)


@comment_routes.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json(silent=True) or {}

    uid = data.get("uid")
    book_id = data.get("book_id")
    comment_text = data.get("comment")

    if uid is None or book_id is None or not comment_text:
        return jsonify({
            "error": "uid, book_id, and comment are required"
        }), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO comments (uid, book_id, comment)
                VALUES (%s, %s, %s)
            """, (uid, book_id, comment_text))

            comment_id = cursor.lastrowid

        connection.commit()

        return jsonify({
            "message": "Comment added successfully",
            "comment": {
                "comment_id": comment_id,
                "uid": uid,
                "book_id": book_id,
                "comment": comment_text
            }
        }), 201

    except Exception as error:
        connection.rollback()
        return jsonify({
            "error": "Unable to create comment",
            "details": str(error)
        }), 500

    finally:
        connection.close()


@comment_routes.route("/books/<int:book_id>/comments", methods=["GET"])
def get_comments(book_id):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT comment_id, uid, book_id, comment
                FROM comments
                WHERE book_id = %s
                ORDER BY comment_id ASC
            """, (book_id,))

            book_comments = cursor.fetchall()

        return jsonify(book_comments), 200

    finally:
        connection.close()


@comment_routes.route("/comments/<int:book_id>", methods=["PUT"])
def update_comment(book_id):
    data = request.get_json(silent=True) or {}

    uid = data.get("uid")
    new_comment = data.get("comment")

    if uid is None or not new_comment:
        return jsonify({
            "error": "uid and comment are required"
        }), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE comments
                SET comment = %s
                WHERE uid = %s AND book_id = %s
            """, (new_comment, uid, book_id))

            if cursor.rowcount == 0:
                return jsonify({"error": "Comment not found"}), 404

        connection.commit()

        return jsonify({
            "message": "Comment updated successfully",
            "comment": {
                "uid": uid,
                "book_id": book_id,
                "comment": new_comment
            }
        }), 200

    finally:
        connection.close()


@comment_routes.route("/comments/<int:book_id>", methods=["DELETE"])
def delete_comment(book_id):
    data = request.get_json(silent=True) or {}
    uid = data.get("uid")

    if uid is None:
        return jsonify({"error": "uid is required"}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM comments
                WHERE uid = %s AND book_id = %s
            """, (uid, book_id))

            if cursor.rowcount == 0:
                return jsonify({"error": "Comment not found"}), 404

        connection.commit()

        return jsonify({
            "message": "Comment deleted successfully"
        }), 200

    finally:
        connection.close()