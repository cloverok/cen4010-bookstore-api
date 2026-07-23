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

@app.route("/books")
def books():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # convert Decimal price to float for JSON
    for r in rows:
        r["price"] = float(r["price"])
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)