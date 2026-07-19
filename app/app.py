from flask import Flask, jsonify

from app.database.schema import initialize_database
from app.routes.rating_routes import rating_routes
from app.routes.comment_routes import comment_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(rating_routes)
    app.register_blueprint(comment_routes)

    @app.route("/")
    def home():
        return jsonify({
            "message": "CEN4010 Bookstore API is running",
            "status": "success"
        })

    return app


app = create_app()


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
