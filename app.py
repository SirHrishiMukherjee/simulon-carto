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

if __name__ == "__main__":
    app.run(debug=True)
