from flask import Flask, jsonify
from profileManagement import profile_bp
from cart import cart_bp
app = Flask(__name__)

app.register_blueprint(profile_bp)
app.register_blueprint(cart_bp)
if __name__ == "__main__":
    app.run(debug=True)