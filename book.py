from db import db


class Book(db.Model):
    __tablename__ = "books"

    isbn = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    publisher = db.Column(db.String(255))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    copies_sold = db.Column(db.Integer)

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