class Book:
    def __init__(
        self,
        isbn,
        title,
        author,
        genre=None,
        publisher=None,
        price=None,
        copies_sold=None,
    ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.publisher = publisher
        self.price = price
        self.copies_sold = copies_sold

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "publisher": self.publisher,
            "price": float(self.price) if self.price is not None else None,
            "copies_sold": self.copies_sold,
        }

    @classmethod
    def from_row(cls, row):
        """
        Creates a Book object from a dictionary row returned by
        cursor(dictionary=True).

        Expected SQL query:

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
        """

        return cls(
            isbn=row["isbn"],
            title=row["title"],
            author=f"{row['first_name']} {row['last_name']}",
            genre=row["genre"],
            publisher=row["publisher"],
            price=row["price"],
            copies_sold=row["copies_sold"],
        )