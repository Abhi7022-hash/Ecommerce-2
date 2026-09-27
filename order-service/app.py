from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import datetime
import os
import requests

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://mongo-service:27017/"
)

USER_SERVICE = os.environ.get(
    "USER_SERVICE_URL",
    "http://user-service:5001"
)

PRODUCT_SERVICE = os.environ.get(
    "PRODUCT_SERVICE_URL",
    "http://product-service:5002"
)

client = MongoClient(MONGO_URI)
db = client["order_db"]
orders = db["orders"]


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def verify_token(token):
    try:
        resp = requests.post(f"{USER_SERVICE}/verify", json={"token": token}, timeout=5)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None


def get_auth_user(request):
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        return verify_token(token)
    return None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "order-service running"}), 200


@app.route("/api/orders", methods=["POST"])
def create_order():
    user_info = get_auth_user(request)
    if not user_info or not user_info.get("valid"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    items = data.get("items", [])  # [{"product_id": "...", "quantity": 2}]
    address = data.get("address", "")

    if not items:
        return jsonify({"error": "No items in order"}), 400

    # Fetch product details
    product_ids = [item["product_id"] for item in items]
    try:
        resp = requests.post(f"{PRODUCT_SERVICE}/products/bulk", json={"ids": product_ids}, timeout=5)
        product_list = resp.json()
    except Exception:
        return jsonify({"error": "Cannot reach product service"}), 503

    product_map = {p["_id"]: p for p in product_list}

    order_items = []
    total = 0
    for item in items:
        pid = item["product_id"]
        qty = item.get("quantity", 1)
        product = product_map.get(pid)
        if not product:
            return jsonify({"error": f"Product {pid} not found"}), 404
        subtotal = product["price"] * qty
        total += subtotal
        order_items.append({
            "product_id": pid,
            "name": product["name"],
            "price": product["price"],
            "quantity": qty,
            "subtotal": subtotal,
        })

    order = {
        "user_id": user_info["user_id"],
        "user_email": user_info["email"],
        "items": order_items,
        "total": total,
        "address": address,
        "status": "placed",
        "created_at": datetime.datetime.utcnow().isoformat(),
    }
    result = orders.insert_one(order)
    order["_id"] = str(result.inserted_id)
    return jsonify({"message": "Order placed successfully", "order": order}), 201


@app.route("/api/orders", methods=["GET"])
def get_orders():
    user_info = get_auth_user(request)
    if not user_info or not user_info.get("valid"):
        return jsonify({"error": "Unauthorized"}), 401

    user_orders = [serialize(o) for o in orders.find({"user_id": user_info["user_id"]})]
    return jsonify(user_orders), 200



    user_info = get_auth_user(request)
    if not user_info or not user_info.get("valid"):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        order = orders.find_one({"_id": ObjectId(order_id), "user_id": user_info["user_id"]})
        if not order:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(serialize(order)), 200
    except Exception:
        return jsonify({"error": "Invalid order ID"}), 400


@app.route("/api/orders/<order_id>/status", methods=["PUT"])
def update_status(order_id):
    data = request.get_json()
    new_status = data.get("status")
    valid_statuses = ["placed", "confirmed", "shipped", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400
    try:
        result = orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": new_status}})
        if result.matched_count == 0:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Status updated"}), 200
    except Exception:
        return jsonify({"error": "Invalid order ID"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
