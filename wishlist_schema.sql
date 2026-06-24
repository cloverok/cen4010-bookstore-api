-- Daniela Martinez
-- Wishlist Management Feature
-- Sprint 2 Database Schema

CREATE DATABASE bookstore;
USE bookstore;

CREATE TABLE User (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE Book (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE Wishlist (
    wishlist_id INT PRIMARY KEY,
    user_id INT,
    wishlist_name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Wishlist_Item (
    wishlist_item_id INT PRIMARY KEY,
    wishlist_id INT,
    book_id INT,
    FOREIGN KEY (wishlist_id) REFERENCES Wishlist(wishlist_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
);

INSERT INTO User (user_id, username, email)
VALUES
(1, 'daniela', 'daniela@email.com');

INSERT INTO Book (book_id, title, author, price)
VALUES
(1, 'The Hobbit', 'J.R.R. Tolkien', 14.99),
(2, '1984', 'George Orwell', 12.50);

INSERT INTO Wishlist (wishlist_id, user_id, wishlist_name)
VALUES
(1, 1, 'Favorites');

INSERT INTO Wishlist_Item (wishlist_item_id, wishlist_id, book_id)
VALUES
(1, 1, 1),
(2, 1, 2);

SELECT * FROM User;
SELECT * FROM Book;
SELECT * FROM Wishlist;
SELECT * FROM Wishlist_Item;


