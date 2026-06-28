from flask import Flask, jsonify
from routes.rating_routes import rating_routes
from routes.comment_routes import comment_routes

app = Flask(__name__)

app.register_blueprint(rating_routes)
app.register_blueprint(comment_routes)

@app.route("/")
def home():
    return jsonify({
        "message": "CEN4010 Bookstore API is running",
        "status": "success"
    })

if __name__ == "__main__":
    app.run(debug=True)