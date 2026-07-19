from flask import Blueprint, jsonify, request
from db import get_db

book_bp = Blueprint("book", __name__)


# ==========================
# Create Book
# ==========================
@book_bp.route("/books", methods=["POST"])
def create_book():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Missing book data"}), 400


    required_fields = [
        "isbn",
        "title",
        "description",
        "price",
        "author",
        "genre",
        "publisher",
        "year_published",
        "copies_sold"
    ]


    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({
                "message": field + " is required"
            }),400


    conn = get_db()
    cursor = conn.cursor(dictionary=True)


    cursor.execute(
        "SELECT isbn FROM books WHERE isbn=%s",
        (data["isbn"],)
    )

    if cursor.fetchone():

        cursor.close()
        conn.close()

        return jsonify({
            "message":"Book with this ISBN already exists"
        }),400



    sql = """
    INSERT INTO books
    (
        isbn,
        title,
        description,
        author,
        price,
        genre,
        publisher,
        year_published,
        copies_sold
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


    values = (
        data["isbn"],
        data["title"],
        data["description"],
        data["author"],
        data["price"],
        data["genre"],
        data["publisher"],
        data["year_published"],
        data["copies_sold"]
    )


    cursor.execute(sql, values)
    conn.commit()


    cursor.close()
    conn.close()


    return jsonify({
        "message":"Book created successfully",
        "book":data
    }),201



# ==========================
# Get Book By ISBN
# ==========================
@book_bp.route("/books/<isbn>", methods=["GET"])
def get_book_by_isbn(isbn):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)


    cursor.execute(
        "SELECT * FROM books WHERE isbn=%s",
        (isbn,)
    )


    book = cursor.fetchone()


    cursor.close()
    conn.close()


    if not book:
        return jsonify({
            "message":"Book not found"
        }),404


    return jsonify(book),200
