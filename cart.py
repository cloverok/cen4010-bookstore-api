from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cm6355582",
        database="bookstore"
    )

@app.route("/cart/<int:user_id>")
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

if __name__ == "__main__":
    app.run(debug=True)