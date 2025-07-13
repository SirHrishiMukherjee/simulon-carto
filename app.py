from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection
client = MongoClient(os.environ.get("MONGO_URI"))
db = client["simulon-maps"]
markers_col = db["markers"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/markers", methods=["GET"])
def get_markers():
    markers = list(markers_col.find({}, {"_id": 0}))
    return jsonify(markers)

@app.route("/api/markers", methods=["POST"])
def add_marker():
    data = request.get_json()
    if "x" in data and "y" in data and "label" in data:
        markers_col.insert_one(data)
        return jsonify({"status": "saved"}), 201
    return jsonify({"error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
