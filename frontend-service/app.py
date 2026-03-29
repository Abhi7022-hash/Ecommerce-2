from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

USER_SERVICE = os.environ.get("USER_SERVICE_URL", "http://localhost:5001")
PRODUCT_SERVICE = os.environ.get("PRODUCT_SERVICE_URL", "http://localhost:5002")
ORDER_SERVICE = os.environ.get("ORDER_SERVICE_URL", "http://localhost:5003")


@app.route("/")
def index():
    return render_template("index.html",
        user_service=USER_SERVICE,
        product_service=PRODUCT_SERVICE,
        order_service=ORDER_SERVICE
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
