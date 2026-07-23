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
    cursor.execute("SELECT book_id FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def user_exists(uid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT uid FROM profile WHERE uid = %s", (uid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

@cart_bp.route("/cart/<int:uid>")
def get_cart(uid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.book_id, b.title,
               CONCAT(a.first_name, ' ', a.last_name) AS author,
               b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON b.book_id = ci.book_id
        JOIN authors a ON a.author_id = b.author_id
        WHERE ci.uid = %s
    """, (uid,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for r in rows:
        r["price"] = float(r["price"])
    return jsonify(rows)

@cart_bp.route("/cart/<int:uid>/subtotal")
def get_subtotal(uid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(b.price * ci.quantity) AS subtotal
        FROM cart_items ci
        JOIN books b ON b.book_id = ci.book_id
        WHERE ci.uid = %s
    """, (uid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    subtotal = float(result[0]) if result[0] is not None else 0.0
    return jsonify({"uid": uid, "subtotal": subtotal})

@cart_bp.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    uid = data.get("uid")
    book_id = data.get("book_id")
    quantity = data.get("quantity", 1)

    if not uid or not book_id:
        return jsonify({"error": "uid and book_id are required"}), 400
    if not user_exists(uid):
        return jsonify({"error": f"uid {uid} does not exist"}), 404
    if not book_exists(book_id):
        return jsonify({"error": f"book_id {book_id} does not exist"}), 404

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cart_items (uid, book_id, quantity) VALUES (%s, %s, %s)",
        (uid, book_id, quantity)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "uid": uid, "book_id": book_id, "quantity": quantity}), 201

@cart_bp.route("/cart", methods=["DELETE"])
def delete_from_cart():
    data = request.get_json()
    uid = data.get("uid")
    book_id = data.get("book_id")

    if not uid or not book_id:
        return jsonify({"error": "uid and book_id are required"}), 400
    if not user_exists(uid):
        return jsonify({"error": f"uid {uid} does not exist"}), 404
    if not book_exists(book_id):
        return jsonify({"error": f"book_id {book_id} does not exist"}), 404

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cart_items WHERE uid = %s AND book_id = %s",
        (uid, book_id)
    )
    conn.commit()
    deleted_count = cursor.rowcount
    cursor.close()
    conn.close()
    if deleted_count == 0:
        return jsonify({"error": "no matching cart item found"}), 404
    return jsonify({"deleted": deleted_count, "uid": uid, "book_id": book_id})
