
# E-Commerce Application on AWS EKS

This is a microservices-based e-commerce application that I deployed on AWS EKS. I built this project to learn how to deploy applications using Docker, Kubernetes, Helm, Terraform, GitHub Actions, and Argo CD.

The application has separate services for the frontend, users, products, and orders. I used MongoDB for storing application data.

## Project Overview

The project contains four microservices:

- **Frontend Service:** Provides the user interface.
- **User Service:** Handles user registration, login, and authentication.
- **Product Service:** Manages product information.
- **Order Service:** Handles order-related operations.

MongoDB is used as the database for the application.

## Technologies Used

| Technology | Purpose |
|---|---|
| AWS EKS | Running the Kubernetes application |
| AWS EC2 | Managing the EKS cluster |
| Terraform | Creating AWS infrastructure |
| Docker | Building container images |
| Docker Hub | Storing Docker images |
| Kubernetes | Managing application containers |
| Helm | Managing Kubernetes manifests |
| GitHub Actions | Building and pushing Docker images |
| Argo CD | Deploying the application using GitOps |
| MongoDB | Application database |
| NGINX Ingress Controller | Routing external traffic to services |

## Architecture

The application uses a microservices architecture. Each service runs in its own container and is deployed separately in Kubernetes.

```text
                  User
                   |
                   v
             NGINX Ingress
                   |
                   v
              Frontend
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   User Service  Product     Order
                 Service    Service
       |           |           |
       +-----------+-----------+
                   |
                   v
                MongoDB
```

## Repository Structure

```text
Ecommerce-2/
│
├── ecommerce-helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── configmap.yaml
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       ├── ingress.yaml
│       ├── mongo-deployment.yaml
│       ├── mongo-pvc.yaml
│       ├── mongo-service.yaml
│       ├── namespace.yaml
│       ├── order-deployment.yaml
│       ├── order-service.yaml
│       ├── product-deployment.yaml
│       ├── product-service.yaml
│       ├── secret.yaml
│       ├── user-deployment.yaml
│       └── user-service.yaml
│
├── frontend-service/
├── user-service/
├── product-service/
├── order-service/
│
├── terraform/
│   ├── access.tf
│   ├── addons.tf
│   ├── eks.tf
│   ├── iam.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── sg.tf
│   ├── terraform.tfvars
│   ├── variables.tf
│   ├── versions.tf
│   └── vpc.tf
│
└── README.md
```

## AWS Infrastructure

I used Terraform to create the AWS infrastructure required for the project.

The infrastructure includes:

- VPC with public and private subnets
- Internet Gateway
- NAT Gateway
- Security Groups
- Amazon EKS cluster
- EKS managed node group
- IAM roles and policies
- EKS add-ons

The application runs on EKS worker nodes inside the cluster.

## CI/CD Workflow

I used GitHub Actions to automate the Docker image build and push process.

The workflow works like this:

1. I make changes to one of the microservices.
2. I push the code to the GitHub repository.
3. GitHub Actions detects which service was changed.
4. It builds the Docker image for that service.
5. The image is pushed to Docker Hub.
6. The image is tagged using the GitHub Actions run number, such as `v1`, `v2`, or `v3`.

Only the changed service image is built and pushed.

### Image Naming

The Docker images are stored in Docker Hub.

```text
abhishek661/frontend
abhishek661/user
abhishek661/product
abhishek661/order
```

Example image tag:

```text
abhishek661/user:v1
```

## GitOps Deployment with Argo CD

I use Argo CD to deploy the application to EKS.

The Helm chart contains the Kubernetes configuration for all the services. Argo CD monitors the GitHub repository and syncs the Helm chart with the cluster.

The deployment flow is:

```text
Code Change
    |
    v
GitHub Actions
    |
    v
Build and Push Docker Image
    |
    v
Update Helm Image Tag in Git
    |
    v
Argo CD Sync
    |
    v
Deploy to EKS
```

This helps keep the Kubernetes deployment configuration in Git.

## Deploying the Helm Chart

To validate the Helm chart:

```bash
helm lint ecommerce-helm
```

To check the rendered Kubernetes manifests:

```bash
helm template ecommerce ecommerce-helm \
  --namespace ecommerce-2
```

To install or upgrade the application manually:

```bash
helm upgrade --install ecommerce ecommerce-helm \
  --namespace ecommerce-2 \
  --create-namespace
```

## Useful Kubernetes Commands

Check the cluster nodes:

```bash
kubectl get nodes
```

Check application pods:

```bash
kubectl get pods -n ecommerce-2
```

Check services:

```bash
kubectl get svc -n ecommerce-2
```

Check Ingress:

```bash
kubectl get ingress -n ecommerce-2
```

Check pod logs:

```bash
kubectl logs <pod-name> -n ecommerce-2
```

Describe a pod:

```bash
kubectl describe pod <pod-name> -n ecommerce-2
```

## What I Learned

While working on this project, I learned how to:

- Create AWS infrastructure using Terraform.
- Deploy an EKS cluster and managed node group.
- Containerize microservices using Docker.
- Deploy applications using Kubernetes and Helm.
- Configure services, Ingress, ConfigMaps, Secrets, and persistent storage.
- Automate Docker image builds and pushes using GitHub Actions.
- Use Argo CD for GitOps-based deployment.
- Troubleshoot Kubernetes pods, services, and application connectivity.

## Future Improvements

- Add monitoring using Prometheus and Grafana.
- Improve application security and secret management.
- Add automated testing to the CI/CD workflow.
