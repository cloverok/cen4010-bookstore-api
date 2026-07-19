from flask import Flask, jsonify
from profileManagement import profile_bp
from wishlist import wishlist_bp
from cart import cart_bp
from app.database.schema import initialize_database
from app.routes.comment_routes import comment_routes
from app.routes.rating_routes import rating_routes

app = Flask(__name__)

# Register feature endpoints in main file
app.register_blueprint(profile_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(rating_routes)
app.register_blueprint(comment_routes)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
