# 🛍️ ShopEasy — Flask Microservices eCommerce

A simple eCommerce application built with **4 Flask microservices** and **MongoDB**.

---

## 📁 Project Structure

```
ecommerce/
├── docker-compose.yml
├── user-service/          # Port 5001 — Auth & Users
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── product-service/       # Port 5002 — Products & Catalog
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── order-service/         # Port 5003 — Orders
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── frontend-service/      # Port 5000 — Web UI
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/style.css
        └── js/app.js
```

---

## 🚀 Run with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Visit the app at:
http://localhost:5000
```

---

## 🛠️ Run Manually (Without Docker)

Make sure MongoDB is running locally on port 27017.

### 1. User Service (Port 5001)
```bash
cd user-service
pip install -r requirements.txt
python app.py
```

### 2. Product Service (Port 5002)
```bash
cd product-service
pip install -r requirements.txt
python app.py
```

### 3. Order Service (Port 5003)
```bash
cd order-service
pip install -r requirements.txt
python app.py
```

### 4. Frontend Service (Port 5000)
```bash
cd frontend-service
pip install -r requirements.txt
python app.py
```

---

## 🔗 API Endpoints

### User Service (5001)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register new user |
| POST | /login | Login, returns JWT token |
| POST | /verify | Verify JWT token |
| GET | /users/:id | Get user by ID |

### Product Service (5002)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products | List all products |
| GET | /products?category=X | Filter by category |
| GET | /products/:id | Get single product |
| POST | /products | Create product |
| PUT | /products/:id | Update product |
| DELETE | /products/:id | Delete product |
| POST | /products/bulk | Fetch multiple by IDs |

### Order Service (5003)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /orders | Place new order (auth required) |
| GET | /orders | List user's orders (auth required) |
| GET | /orders/:id | Get order detail (auth required) |
| PUT | /orders/:id/status | Update order status |

---

## 🗄️ MongoDB Databases

| Service | Database | Collection |
|---------|----------|------------|
| user-service | user_db | users |
| product-service | product_db | products |
| order-service | order_db | orders |

---

## ✨ Features

- ✅ User registration & login with JWT authentication
- ✅ Browse products with category filter
- ✅ Add to cart (localStorage based)
- ✅ Place orders with delivery address
- ✅ View order history with status
- ✅ 8 sample products auto-seeded on startup
- ✅ Responsive UI (mobile-friendly)
- ✅ Inter-service communication via REST APIs
