from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

USER_SERVICE = os.environ.get("USER_SERVICE_URL", "/api/users")
PRODUCT_SERVICE = os.environ.get("PRODUCT_SERVICE_URL", "/api/products")
ORDER_SERVICE = os.environ.get("ORDER_SERVICE_URL", "/api/orders")


@app.route("/health", methods=["GET"])
def health():
    return {"status": "frontend-service running"}, 200


@app.route("/")
def index():
    return render_template("index.html",
        user_service=USER_SERVICE,
        product_service=PRODUCT_SERVICE,
        order_service=ORDER_SERVICE
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
