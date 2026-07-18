from flask import Flask, jsonify

from profileManagement import profile_bp
from wishlist import wishlist_bp

app = Flask(__name__)

# Register feature endpoint in main file
app.register_blueprint(profile_bp)
app.register_blueprint(wishlist_bp)

if __name__ == "__main__":
    app.run(debug=True)