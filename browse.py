from flask import Blueprint, jsonify, request
<<<<<<< Updated upstream
from book import Book
=======
from db import get_db
from book import Book

>>>>>>> Stashed changes

browse_bp = Blueprint(
    "browse",
    __name__,
    url_prefix="/books"
)

MAX_LIMIT = 50


# Get books by genre
@browse_bp.route("/genre/<string:genre>", methods=["GET"])
def get_books_by_genre(genre):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT
                isbn,
                title,
                author,
                genre,
                publisher,
                price,
                rating,
                copies_sold
            FROM books
            WHERE genre LIKE %s
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


# Browse, filter, sort, and paginate books
@browse_bp.route("/", methods=["GET"])
def browse_books():

    # Get query parameters
    isbn = request.args.get("isbn")
    title = request.args.get("title")
    genre = request.args.get("genre")
    author = request.args.get("author")
    publisher = request.args.get("publisher")

    sort = request.args.get("sort")
    order = request.args.get("order", "asc").lower()

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)


    # Validate pagination
    if page < 1 or limit < 1:
        return jsonify({
            "success": False,
            "message": "Page and limit must be greater than zero."
        }), 400

    # Prevent excessively large requests
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT


    # Validate sorting order
    if order not in ["asc", "desc"]:
        return jsonify({
            "success": False,
            "message": "Order must be either 'asc' or 'desc'."
        }), 400


    # Allowed sorting fields
    valid_fields = {
        "title": "title",
        "author": "author",
        "price": "price",
        "rating": "rating",
        "copies_sold": "copies_sold"
    }


    # Validate sorting field
    if sort and sort not in valid_fields:
        return jsonify({
            "success": False,
            "message": "Invalid sort field.",
            "valid_fields": list(valid_fields.keys())
        }), 400


    # Build SQL query
    base_query = """
        FROM books
        WHERE 1=1
    """

    conditions = []
    parameters = []


    # Filters
    if isbn:
        conditions.append("AND isbn = %s")
        parameters.append(isbn)

    if title:
        conditions.append("AND title LIKE %s")
        parameters.append(f"%{title}%")

    if genre:
        conditions.append("AND genre LIKE %s")
        parameters.append(f"%{genre}%")

    if author:
        conditions.append("AND author LIKE %s")
        parameters.append(f"%{author}%")

    if publisher:
        conditions.append("AND publisher LIKE %s")
        parameters.append(f"%{publisher}%")


    # Sorting
    if sort:
        sort_column = valid_fields[sort]
        sort_order = "DESC" if order == "desc" else "ASC"

        order_clause = f" ORDER BY {sort_column} {sort_order}"

    else:
        # Default sorting
        order_clause = " ORDER BY title ASC"


    # Connect to database
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:

        # Count total matching books
        count_query = """
            SELECT COUNT(*) AS total
        """ + base_query + " " + " ".join(conditions)

        cursor.execute(count_query, tuple(parameters))

        result = cursor.fetchone()
        total_books = result["total"]


        # Return 404 if no books match
        if total_books == 0:
            return jsonify({
                "success": False,
                "message": "No books matched the supplied filters.",
                "filters": {
                    "isbn": isbn,
                    "title": title,
                    "genre": genre,
                    "author": author,
                    "publisher": publisher
                }
            }), 404


        # Calculate pagination
        total_pages = (total_books + limit - 1) // limit

        offset = (page - 1) * limit


        # Get requested books
        books_query = """
            SELECT
                isbn,
                title,
                author,
                genre,
                publisher,
                price,
                rating,
                copies_sold
        """ + base_query + " " + " ".join(conditions)

        books_query += order_clause
        books_query += " LIMIT %s OFFSET %s"


        book_parameters = parameters + [limit, offset]

        cursor.execute(
            books_query,
            tuple(book_parameters)
        )

        rows = cursor.fetchall()


        books = [
            Book.from_row(row).to_dict()
            for row in rows
        ]


        # Return response
        return jsonify({
            "success": True,
            "page": page,
            "limit": limit,
            "pages": total_pages,
            "total_books": total_books,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "books": books
        }), 200

    finally:
        cursor.close()
        db.close()