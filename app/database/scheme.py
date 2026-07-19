from .db import get_db_connection

def initialize_rating_comment_schema():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    rating_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    book_id INT NOT NULL,
                    rating INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT chk_rating_range
                        CHECK (rating BETWEEN 1 AND 5),
                    CONSTRAINT uq_user_book_rating
                        UNIQUE (user_id, book_id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    comment_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    book_id INT NOT NULL,
                    comment TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP
                )
            """)

        connection.commit()
        print("Rating and commenting tables are ready.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()