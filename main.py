from flask import Flask, jsonify

from profileManagement import profile_bp

app = Flask(__name__)

# Register feature endpoint in main file
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)



    