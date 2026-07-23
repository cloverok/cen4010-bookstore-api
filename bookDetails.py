from flask import Blueprint, jsonify, request
from db import get_db

book_bp = Blueprint("book", __name__)


# ==================================================
# Create Book
# ==================================================
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
        "author_id",
        "genre",
        "publisher",
        "year_published",
        "copies_sold"
    ]


    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({
                "message": field + " is required"
            }), 400


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
            "message": "Book with this ISBN already exists"
        }), 400



    sql = """
    INSERT INTO books
    (
        isbn,
        title,
        description,
        price,
        author_id,
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
        data["price"],
        data["author_id"],
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
        "message": "Book created successfully",
        "book": data
    }), 201



# ==================================================
# Get Book By ISBN
# ==================================================
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
            "message": "Book not found"
        }), 404


    return jsonify(book), 200



# ==================================================
# Create Author
# ==================================================
@book_bp.route("/authors", methods=["POST"])
def create_author():

    data = request.get_json(silent=True)


    if not data:
        return jsonify({
            "message": "Missing author data"
        }), 400



    required_fields = [
        "first_name",
        "last_name",
        "biography",
        "publisher"
    ]


    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({
                "message": field + " is required"
            }), 400



    conn = get_db()
    cursor = conn.cursor(dictionary=True)



    sql = """
    INSERT INTO authors
    (
        first_name,
        last_name,
        biography,
        publisher
    )
    VALUES
    (%s,%s,%s,%s)
    """



    values = (
        data["first_name"],
        data["last_name"],
        data["biography"],
        data["publisher"]
    )



    cursor.execute(sql, values)
    conn.commit()


    cursor.close()
    conn.close()



    return jsonify({
        "message": "Author created successfully",
        "author": data
    }), 201



# ==================================================
# Get Books By Author
# ==================================================
@book_bp.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)



    cursor.execute(
        "SELECT * FROM books WHERE author_id=%s",
        (author_id,)
    )


    books = cursor.fetchall()



    cursor.close()
    conn.close()



    if not books:
        return jsonify({
            "message": "No books found for this author"
        }), 404



    return jsonify(books), 200
