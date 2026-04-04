# eCommerce Microservices App

A simple eCommerce web app built using microservices architecture.
I built this project to learn and practice Docker, Kubernetes and AWS.

## What This Project Does

Users can register, login, browse products, add to cart and place orders.
Instead of building everything in one app, I split it into 4 small services
where each service handles one specific job.

## Services

- **user-service** – handles registration and login (JWT authentication)
- **product-service** – handles products and catalog
- **order-service** – handles placing and viewing orders
- **frontend-service** – serves the web UI (HTML, CSS, JS)

## Tech Stack

- Python, Flask, MongoDB
- Docker (multi-stage builds)
- Kubernetes
- AWS EKS, EC2, EBS, VPC, IAM
- Terraform
- NGINX Ingress Controller

## Project Structure
ecommerce/
├── user-service/
├── product-service/
├── order-service/
├── frontend-service/
├── k8s/
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   ├── secrets/
│   ├── pvc/
│   └── ingress/
└── terraform/

## How I Deployed This

1. Wrote Terraform files to create AWS infrastructure (VPC, EKS, EC2 nodes)
2. Built Docker images using multi-stage Dockerfiles
3. Pushed images to Docker Hub
4. Connected kubectl to EKS cluster
5. Applied all Kubernetes YAML files
6. Installed NGINX Ingress Controller for routing

## How to Run Locally

Make sure MongoDB is running on your machine.
```bash
# Run each service in separate terminal
cd user-service && pip install -r requirements.txt && python app.py
cd product-service && pip install -r requirements.txt && python app.py
cd order-service && pip install -r requirements.txt && python app.py
cd frontend-service && pip install -r requirements.txt && python app.py
```

Open browser at `http://localhost:5000`

## What I Learned

- How to split an app into microservices
- How to write multi-stage Dockerfiles
- How Kubernetes manages containers
- How to provision AWS infrastructure using Terraform
- How NGINX Ingress routes traffic to different services
