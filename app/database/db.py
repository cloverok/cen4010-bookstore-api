import os

import pymysql
from pymysql.cursors import DictCursor


def get_db_connection():
    """Create and return a connection to the bookstore database."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bookstore"),
        cursorclass=DictCursor,
        autocommit=False
    )