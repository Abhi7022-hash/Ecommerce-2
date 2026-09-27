from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import datetime
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://mongo-service:27017/"
)

client = MongoClient(MONGO_URI)
db = client["product_db"]
products = db["products"]


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def seed_products():
    if products.count_documents({}) == 0:
        sample = [
            {"name": "Wireless Headphones", "description": "High quality Bluetooth headphones with noise cancellation", "price": 2999, "category": "Electronics", "stock": 50, "image": "🎧"},
            {"name": "Running Shoes", "description": "Lightweight and breathable running shoes for all terrains", "price": 1499, "category": "Footwear", "stock": 30, "image": "👟"},
            {"name": "Backpack", "description": "Durable 30L backpack with laptop compartment", "price": 899, "category": "Bags", "stock": 20, "image": "🎒"},
            {"name": "Smart Watch", "description": "Feature-packed smartwatch with health tracking", "price": 4999, "category": "Electronics", "stock": 15, "image": "⌚"},
            {"name": "Coffee Maker", "description": "Automatic drip coffee maker with timer", "price": 1299, "category": "Kitchen", "stock": 25, "image": "☕"},
            {"name": "Sunglasses", "description": "UV400 polarized sunglasses with stylish frame", "price": 599, "category": "Accessories", "stock": 40, "image": "🕶️"},
            {"name": "Yoga Mat", "description": "Non-slip eco-friendly yoga mat, 6mm thick", "price": 499, "category": "Sports", "stock": 35, "image": "🧘"},
            {"name": "Notebook Set", "description": "Pack of 3 premium hardcover notebooks", "price": 299, "category": "Stationery", "stock": 60, "image": "📓"},
        ]
        for p in sample:
            p["created_at"] = datetime.datetime.utcnow().isoformat()
        products.insert_many(sample)
        print("Sample products seeded.")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "product-service running"}), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    category = request.args.get("category")
    query = {}
    if category:
        query["category"] = category
    result = [serialize(p) for p in products.find(query)]
    return jsonify(result), 200


@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(serialize(product)), 200
    except Exception:
        return jsonify({"error": "Invalid product ID"}), 400


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    required = ["name", "description", "price", "category", "stock"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    data["created_at"] = datetime.datetime.utcnow().isoformat()
    data["image"] = data.get("image", "📦")
    result = products.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return jsonify(data), 201


@app.route("/api/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.get_json()
        data.pop("_id", None)
        result = products.update_one({"_id": ObjectId(product_id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Product not found"}), 404
        updated = products.find_one({"_id": ObjectId(product_id)})
        return jsonify(serialize(updated)), 200
    except Exception:
        return jsonify({"error": "Invalid product ID"}), 400


@app.route("/api/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        result = products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product deleted"}), 200
    except Exception:
        return jsonify({"error": "Invalid product ID"}), 400

@app.route("/api/products/bulk", methods=["POST"])
def get_products_by_ids():
    data = request.get_json()
    ids = data.get("ids", [])
    try:
        object_ids = [ObjectId(i) for i in ids]
        result = [serialize(p) for p in products.find({"_id": {"$in": object_ids}})]
        return jsonify(result), 200
    except Exception:
        return jsonify({"error": "Invalid IDs"}), 400


if __name__ == "__main__":
    seed_products()
    app.run(host="0.0.0.0", port=5002, debug=False)
