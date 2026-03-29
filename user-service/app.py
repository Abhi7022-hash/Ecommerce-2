from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.environ.get("SECRET_KEY", "ecommerce-secret-key")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["user_db"]
users = db["users"]


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "user-service running"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "All fields required"}), 400

    if users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = {
        "name": name,
        "email": email,
        "password": hashed.decode(),
        "created_at": datetime.datetime.utcnow().isoformat(),
    }
    result = users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    del user["password"]
    return jsonify({"message": "User registered", "user": user}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify(
        {
            "token": token,
            "user": {"id": str(user["_id"]), "name": user["name"], "email": user["email"]},
        }
    ), 200


@app.route("/verify", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "user_id": payload["user_id"], "email": payload["email"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        del user["password"]
        return jsonify(serialize(user)), 200
    except Exception:
        return jsonify({"error": "Invalid user ID"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
