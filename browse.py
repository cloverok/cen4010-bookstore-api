from flask import Blueprint, jsonify, request
from models.book import Book

browse_bp = Blueprint(
    "browse",
    __name__,
    url_prefix="/books"
)

MAX_LIMIT = 50


# Existing endpoint
@browse_bp.route("/genre/<genre>", methods=["GET"])
def get_books_by_genre(genre):

    books = Book.query.filter(Book.genre.ilike(f"%{genre}%")).all()

    if not books:
        return jsonify({
            "success": False,
            "message": "No books found for this genre."
        }), 404

    return jsonify({
        "success": True,
        "count": len(books),
        "books": [book.to_dict() for book in books]
    })


# Browse endpoint
@browse_bp.route("/", methods=["GET"])
def browse_books():

    query = Book.query

    
    # Filters
    

    isbn = request.args.get("isbn")
    title = request.args.get("title")
    genre = request.args.get("genre")
    author = request.args.get("author")
    publisher = request.args.get("publisher")

    if isbn:
        query = query.filter(Book.isbn == isbn)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    if publisher:
        query = query.filter(Book.publisher.ilike(f"%{publisher}%"))

    
    # Sorting
    

    sort = request.args.get("sort")
    order = request.args.get("order", "asc").lower()

    valid_fields = {
        "title": Book.title,
        "author": Book.author,
        "price": Book.price,
        "rating": Book.rating,
        "copies_sold": Book.copies_sold
    }

    if order not in ["asc", "desc"]:
        return jsonify({
            "success": False,
            "message": "Order must be either 'asc' or 'desc'."
        }), 400

    if sort:

        if sort not in valid_fields:
            return jsonify({
                "success": False,
                "message": "Invalid sort field.",
                "valid_fields": list(valid_fields.keys())
            }), 400

        column = valid_fields[sort]

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    else:
        # Default sort
        query = query.order_by(Book.title.asc())

    
    # Pagination
    

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    if page < 1 or limit < 1:
        return jsonify({
            "success": False,
            "message": "Page and limit must be greater than zero."
        }), 400

    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    books = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    
    # No Results
    

    if books.total == 0:
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

    
    # Response
    

    return jsonify({
        "success": True,
        "page": page,
        "limit": limit,
        "pages": books.pages,
        "total_books": books.total,
        "has_next": books.has_next,
        "has_prev": books.has_prev,
        "books": [book.to_dict() for book in books.items]
    })