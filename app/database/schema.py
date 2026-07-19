import os
from pathlib import Path

import pymysql


def initialize_database():
    """Create the bookstore database and run the shared schema on startup."""
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "bookstore")

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        autocommit=False,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database.replace('`', '``')}`"
            )
            cursor.execute(f"USE `{database.replace('`', '``')}`")

            schema_path = Path(__file__).resolve().parents[2] / "schema.sql"
            schema_sql = schema_path.read_text(encoding="utf-8")

            for statement in schema_sql.split(";"):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

        connection.commit()
        print("Bookstore database tables are ready.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# Kept as a compatibility alias for older feature-branch commands.
initialize_rating_comment_schema = initialize_database
