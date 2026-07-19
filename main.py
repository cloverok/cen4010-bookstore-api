from flask import Flask, jsonify
from profileManagement import profile_bp
from wishlist import wishlist_bp
from cart import cart_bp
from bookDetails import book_bp

app = Flask(__name__)

# Register feature endpoints in main file
app.register_blueprint(profile_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(book_bp)

if __name__ == "__main__":
    app.run(debug=True)
