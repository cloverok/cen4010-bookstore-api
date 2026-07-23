<<<<<<< Updated upstream
from db import db
=======
from db import get_db
>>>>>>> Stashed changes


class Book:
    def __init__(
        self,
        isbn,
        title,
        author,
        genre=None,
        publisher=None,
        price=None,
        rating=None,
        copies_sold=None
    ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.publisher = publisher
        self.price = price
        self.rating = rating
        self.copies_sold = copies_sold

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "publisher": self.publisher,
            "price": self.price,
            "rating": self.rating,
            "copies_sold": self.copies_sold
        }

    @staticmethod
    def from_row(row):
        return Book(
            isbn=row["isbn"],
            title=row["title"],
            author=row["author"],
            genre=row.get("genre"),
            publisher=row.get("publisher"),
            price=row.get("price"),
            rating=row.get("rating"),
            copies_sold=row.get("copies_sold")
        )