from flask import Blueprint, jsonify, request
from book import Book
from db import get_db

browse_bp = Blueprint(
    "browse",
    __name__,
    url_prefix="/books"
)

MAX_LIMIT = 50


@browse_bp.route("/", methods=["GET"])
def browse_books():

    isbn = request.args.get("isbn")
    title = request.args.get("title")
    genre = request.args.get("genre")
    author = request.args.get("author")
    publisher = request.args.get("publisher")

    sort = request.args.get("sort")
    order = request.args.get("order", "asc").lower()

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    if page < 1 or limit < 1:
        return jsonify({
            "success": False,
            "message": "Page and limit must be greater than zero."
        }), 400

    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    if order not in ["asc", "desc"]:
        return jsonify({
            "success": False,
            "message": "Order must be 'asc' or 'desc'."
        }), 400

    valid_fields = {
        "title": "b.title",
        "author": "CONCAT(a.first_name, ' ', a.last_name)",
        "genre": "b.genre",
        "publisher": "b.publisher",
        "price": "b.price",
        "copies_sold": "b.copies_sold"
    }

    if sort and sort not in valid_fields:
        return jsonify({
            "success": False,
            "message": "Invalid sort field.",
            "valid_fields": list(valid_fields.keys())
        }), 400

    base_query = """
        FROM books b
        JOIN authors a
            ON b.author_id = a.author_id
        WHERE 1=1
    """

    conditions = []
    parameters = []

    if isbn:
        conditions.append("AND b.isbn = %s")
        parameters.append(isbn)

    if title:
        conditions.append("AND b.title LIKE %s")
        parameters.append(f"%{title}%")

    if genre:
        conditions.append("AND b.genre LIKE %s")
        parameters.append(f"%{genre}%")

    if publisher:
        conditions.append("AND b.publisher LIKE %s")
        parameters.append(f"%{publisher}%")

    if author:
        conditions.append(
            "AND CONCAT(a.first_name, ' ', a.last_name) LIKE %s"
        )
        parameters.append(f"%{author}%")

    if sort:
        order_clause = f" ORDER BY {valid_fields[sort]} {'DESC' if order == 'desc' else 'ASC'}"
    else:
        order_clause = " ORDER BY b.title ASC"

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:

        count_query = """
            SELECT COUNT(*) AS total
        """ + base_query + " " + " ".join(conditions)

        cursor.execute(count_query, tuple(parameters))
        total_books = cursor.fetchone()["total"]

        if total_books == 0:
            return jsonify({
                "success": False,
                "message": "No books matched the supplied filters."
            }), 404

        total_pages = (total_books + limit - 1) // limit
        offset = (page - 1) * limit

        books_query = """
            SELECT
                b.isbn,
                b.title,
                a.first_name,
                a.last_name,
                b.genre,
                b.publisher,
                b.price,
                b.copies_sold
        """ + base_query + " " + " ".join(conditions)

        books_query += order_clause
        books_query += " LIMIT %s OFFSET %s"

        cursor.execute(
            books_query,
            tuple(parameters + [limit, offset])
        )

        rows = cursor.fetchall()

        books = [
            Book.from_row(row).to_dict()
            for row in rows
        ]

        return jsonify({
            "success": True,
            "page": page,
            "pages": total_pages,
            "limit": limit,
            "total_books": total_books,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "books": books
        }), 200

    finally:
        cursor.close()
        db.close()


@browse_bp.route("/genre/<string:genre>", methods=["GET"])
def get_books_by_genre(genre):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:

        query = """
            SELECT
                b.isbn,
                b.title,
                a.first_name,
                a.last_name,
                b.genre,
                b.publisher,
                b.price,
                b.copies_sold
            FROM books b
            JOIN authors a
                ON b.author_id = a.author_id
            WHERE b.genre LIKE %s
            ORDER BY b.title
        """

        cursor.execute(query, (f"%{genre}%",))

        rows = cursor.fetchall()

        books = [
            Book.from_row(row).to_dict()
            for row in rows
        ]

        if not books:
            return jsonify({
                "success": False,
                "message": "No books found for this genre."
            }), 404

        return jsonify({
            "success": True,
            "count": len(books),
            "books": books
        }), 200

    finally:
        cursor.close()
        db.close()