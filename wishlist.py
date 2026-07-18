from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error, IntegrityError


wishlist_bp = Blueprint("wishlist", __name__)


# Connect to your local MySQL database
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bookstore"
    )


# Create a new wishlist
# POST /wishlist
@wishlist_bp.route("/wishlist", methods=["POST"])
def create_wishlist():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Wishlist data JSON is empty."}), 400

    user_id = data.get("user_id")
    wishlist_name = data.get("wishlist_name")

    if not user_id or not wishlist_name:
        return jsonify({
            "error": "user_id and wishlist_name are required."
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Make sure the user exists
        cursor.execute(
            "SELECT uid FROM profile WHERE uid = %s",
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "User not found."}), 404

        # Create the wishlist
        cursor.execute(
            """
            INSERT INTO wishlist (uid, wishlist_name)
            VALUES (%s, %s)
            """,
            (user_id, wishlist_name)
        )

        conn.commit()

        wishlist_id = cursor.lastrowid

        return jsonify({
            "success": "Wishlist created successfully.",
            "wishlist_id": wishlist_id,
            "user_id": user_id,
            "wishlist_name": wishlist_name
        }), 201

    except Error as error:
        return jsonify({
            "error": "Unable to create wishlist.",
            "details": str(error)
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()


# Add a book to a wishlist
# POST /wishlist/book
@wishlist_bp.route("/wishlist/book", methods=["POST"])
def add_book_to_wishlist():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Wishlist item data JSON is empty."}), 400

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if not wishlist_id or not book_id:
        return jsonify({
            "error": "wishlist_id and book_id are required."
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Make sure the wishlist exists
        cursor.execute(
            "SELECT wishlist_id FROM wishlist WHERE wishlist_id = %s",
            (wishlist_id,)
        )

        wishlist = cursor.fetchone()

        if wishlist is None:
            return jsonify({"error": "Wishlist not found."}), 404

        # Make sure the book exists
        cursor.execute(
            "SELECT book_id FROM books WHERE book_id = %s",
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            return jsonify({"error": "Book not found."}), 404

        # Check whether the book is already in the wishlist
        cursor.execute(
            """
            SELECT wishlist_item_id
            FROM wishlist_item
            WHERE wishlist_id = %s AND book_id = %s
            """,
            (wishlist_id, book_id)
        )

        existing_item = cursor.fetchone()

        if existing_item is not None:
            return jsonify({
                "error": "Book is already in this wishlist."
            }), 409

        # Add the book
        cursor.execute(
            """
            INSERT INTO wishlist_item (wishlist_id, book_id)
            VALUES (%s, %s)
            """,
            (wishlist_id, book_id)
        )

        conn.commit()

        wishlist_item_id = cursor.lastrowid

        return jsonify({
            "success": "Book added to wishlist successfully.",
            "wishlist_item_id": wishlist_item_id,
            "wishlist_id": wishlist_id,
            "book_id": book_id
        }), 201

    except IntegrityError as error:
        return jsonify({
            "error": "Book is already in this wishlist.",
            "details": str(error)
        }), 409

    except Error as error:
        return jsonify({
            "error": "Unable to add book to wishlist.",
            "details": str(error)
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()


# Remove a book from a wishlist
# DELETE /wishlist/book
@wishlist_bp.route("/wishlist/book", methods=["DELETE"])
def remove_book_from_wishlist():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Wishlist item data JSON is empty."}), 400

    wishlist_id = data.get("wishlist_id")
    book_id = data.get("book_id")

    if not wishlist_id or not book_id:
        return jsonify({
            "error": "wishlist_id and book_id are required."
        }), 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM wishlist_item
            WHERE wishlist_id = %s AND book_id = %s
            """,
            (wishlist_id, book_id)
        )

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Book was not found in this wishlist."
            }), 404

        conn.commit()

        return jsonify({
            "success": "Book removed from wishlist successfully.",
            "wishlist_id": wishlist_id,
            "book_id": book_id
        }), 200

    except Error as error:
        return jsonify({
            "error": "Unable to remove book from wishlist.",
            "details": str(error)
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()


# Retrieve all books from a wishlist
# GET /wishlist/<wishlist_id>
@wishlist_bp.route("/wishlist/<int:wishlist_id>", methods=["GET"])
def get_wishlist(wishlist_id):
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Make sure the wishlist exists
        cursor.execute(
            """
            SELECT wishlist_id, uid, wishlist_name
            FROM wishlist
            WHERE wishlist_id = %s
            """,
            (wishlist_id,)
        )

        wishlist = cursor.fetchone()

        if wishlist is None:
            return jsonify({"error": "Wishlist not found."}), 404

        # Retrieve every book in the wishlist
        cursor.execute(
            """
            SELECT books.*
            FROM books
            INNER JOIN wishlist_item
                ON books.book_id = wishlist_item.book_id
            WHERE wishlist_item.wishlist_id = %s
            """,
            (wishlist_id,)
        )

        books = cursor.fetchall()

        return jsonify({
            "wishlist_id": wishlist["wishlist_id"],
            "user_id": wishlist["uid"],
            "wishlist_name": wishlist["wishlist_name"],
            "books": books
        }), 200

    except Error as error:
        return jsonify({
            "error": "Unable to retrieve wishlist.",
            "details": str(error)
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()