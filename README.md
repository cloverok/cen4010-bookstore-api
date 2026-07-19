# CEN 4010 - Bookstore RESTful API

A group project for CEN 4010: a RESTful API for a fictitious online bookstore.
Built as a single web service where each team member owns one feature.

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** MySQL
- **API Testing:** Postman

## Team & Feature Ownership

Each member owns one feature and implements its four HTTP endpoints.

| Feature | Owner |
| --- | --- |
| Book Browsing and Sorting | Bryan |
| Book Details | Riley |
| Profile Management | Ben |
| Shopping Cart | Clive |
| Book Rating and Commenting | Peter |
| Wish List Management | Daniela |

## Endpoints by Feature

**Book Browsing and Sorting**
- `GET` books by genre
- `GET` top 10 best-selling books
- `GET` books with a rating equal to or higher than a given value
- `PUT/PATCH` apply a discount percent to all books from a given publisher

**Book Details**
- `POST` create a book (ISBN, name, description, price, author, genre, publisher, year, copies sold)
- `GET` a book's details by ISBN
- `POST` create an author (first name, last name, biography, publisher)
- `GET` the list of books by a given author

**Profile Management**
- `POST` create a user (username, password, optional name/email/address)
- `GET` a user's details by username
- `PUT/PATCH` update any user field (except email)
- `POST` add a credit card to a user

**Shopping Cart**
- `GET` the subtotal of all items in a user's cart
- `POST` add a book to a user's cart
- `GET` the list of books in a user's cart
- `DELETE` a book from a user's cart

**Book Rating and Commenting**
- `POST` a 5-star rating for a book by a user
- `POST` a comment for a book by a user
- `GET` all comments for a book
- `GET` the average rating for a book

**Wish List Management**
- `POST` create a named wishlist for a user
- `POST` add a book to a wishlist
- `DELETE` remove a book from a wishlist
- `GET` the books in a wishlist

## Scrum Roles

Roles rotate every sprint.

| Sprint | Scrum Master | Product Owner |
| --- | --- | --- |
| Sprint 1 | Clive | Riley |
| Sprint 2 | Ben | Peter |
| Sprint 3 | Daniela | Bryan |
| Sprint 4 | Peter | Ben |
| Sprint 5 | Clive | Riley |

## Branch Workflow

- `main` is the stable, integrated branch.
- Each member creates a feature branch each sprint (e.g. `clive-cart`), commits their work there, then merges into `main` at the end of the sprint.

## Getting Started (local setup)

> To be completed in Sprint 2 once the database and first endpoint are in place.

```bash
# 1. Clone the repo
git clone https://github.com/cloverok/cen4010-bookstore-api.git
cd cen4010-bookstore-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (To be added) configure the MySQL connection and run the app
# flask run
```
