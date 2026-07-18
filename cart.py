from flask import Blueprint, jsonify, request
import mysql.connector

cart_bp = Blueprint("cart", __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cm6355582",
        database="bookstore"
    )

def book_exists(book_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def user_exists(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

@cart_bp.route("/cart/<int:user_id>")
def get_cart(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id, b.title, b.author, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON b.id = ci.book_id
        WHERE ci.user_id = %s
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for r in rows:
        r["price"] = float(r["price"])
    return jsonify(rows)

@cart_bp.route("/cart/<int:user_id>/subtotal")
def get_subtotal(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(b.price * ci.quantity) AS subtotal
        FROM cart_items ci
        JOIN books b ON b.id = ci.book_id
        WHERE ci.user_id = %s
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    subtotal = float(result[0]) if result[0] is not None else 0.0
    return jsonify({"user_id": user_id, "subtotal": subtotal})

@cart_bp.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    quantity = data.get("quantity", 1)

    if not user_id or not book_id:
        return jsonify({"error": "user_id and book_id are required"}), 400
    if not user_exists(user_id):
        return jsonify({"error": f"user_id {user_id} does not exist"}), 404
    if not book_exists(book_id):
        return jsonify({"error": f"book_id {book_id} does not exist"}), 404

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cart_items (user_id, book_id, quantity) VALUES (%s, %s, %s)",
        (user_id, book_id, quantity)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "user_id": user_id, "book_id": book_id, "quantity": quantity}), 201

@cart_bp.route("/cart", methods=["DELETE"])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not user_id or not book_id:
        return jsonify({"error": "user_id and book_id are required"}), 400
    if not user_exists(user_id):
        return jsonify({"error": f"user_id {user_id} does not exist"}), 404
    if not book_exists(book_id):
        return jsonify({"error": f"book_id {book_id} does not exist"}), 404

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cart_items WHERE user_id = %s AND book_id = %s",
        (user_id, book_id)
    )
    conn.commit()
    deleted_count = cursor.rowcount
    cursor.close()
    conn.close()
    if deleted_count == 0:
        return jsonify({"error": "no matching cart item found"}), 404
    return jsonify({"deleted": deleted_count, "user_id": user_id, "book_id": book_id})