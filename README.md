# FitBook - Online Training Booking System

A complete DevOps student project demonstrating a full CI/CD pipeline with Docker, Kubernetes, and Argo CD.

## 📋 Project Overview

FitBook is a simple yet powerful online training booking system showcasing modern DevOps practices. Users can browse trainers, view available training sessions, and book their preferred training slots.

## 🏗️ Architecture test

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
┌────────────────────────▼────────────────────────────────────┐
│                   Nginx (Frontend)                           │
│              React + Vite SPA                                │
└────────────────────────┬────────────────────────────────────┘
                         │ API Calls (/api)
┌────────────────────────▼────────────────────────────────────┐
│                 FastAPI Backend                              │
│            RESTful API Endpoints                             │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
┌────────────────────────▼────────────────────────────────────┐
│                    PostgreSQL                                │
│               Training Data Storage                          │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Frontend**: React 18 + Vite + Axios
- **Backend**: Python FastAPI + SQLAlchemy + Uvicorn
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (Minikube)
- **CI/CD**: GitHub Actions
- **GitOps**: Argo CD
- **Registry**: Docker Hub

## 📚 Key Features

- **List Trainers**: Browse all available fitness trainers
- **View Training Slots**: Check available training sessions
- **Book Training**: Reserve a training slot with client name
- **Manage Bookings**: View all bookings and cancel if needed
- **Health Checks**: Endpoint monitoring for all services

## 🗄️ Database Schema

### trainers
- `id` (Integer, Primary Key)
- `name` (String) - Trainer's full name
- `specialization` (String) - Area of expertise (Yoga, Pilates, etc.)

### training_slots
- `id` (Integer, Primary Key)
- `trainer_id` (Foreign Key) - Reference to trainer
- `training_date` (DateTime) - When the training is scheduled
- `is_available` (Boolean) - Availability status

### bookings
- `id` (Integer, Primary Key)
- `client_name` (String) - Name of the person booking
- `training_slot_id` (Foreign Key) - Reference to training slot
- `created_at` (DateTime) - When the booking was made

## 🚀 Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/fitbook.git
   cd fitbook
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings if needed
   ```

3. **Start the application**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Stop the application**
   ```bash
   docker compose down
   ```

## 🔌 API Endpoints

All endpoints are prefixed with `/api`

- `GET /health` - Health check
- `GET /trainers` - List all trainers
- `GET /slots` - List all training slots
- `GET /slots/available` - List available slots
- `POST /bookings` - Create a booking
  - Request body: `{"client_name": "string", "training_slot_id": integer}`
- `GET /bookings` - List all bookings
- `DELETE /bookings/{id}` - Cancel a booking

## 📦 Repository Structure

```
fitbook/
├── frontend/                    # React + Vite application
│   ├── src/
│   │   ├── pages/              # React pages
│   │   ├── App.jsx             # Main component
│   │   ├── main.jsx            # Entry point
│   │   └── api.js              # API client
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── index.html
├── backend/                     # FastAPI application
│   ├── main.py                 # FastAPI app
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── crud.py                 # Database operations
│   ├── database.py             # DB configuration
│   ├── config.py               # App configuration
│   ├── test_main.py            # Tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── kubernetes/                  # K8s manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── postgres-statefulset.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── ingress.yaml
├── argocd/                      # Argo CD configuration
│   └── application.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions workflow
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 GitHub Actions CI/CD Configuration

### Setup Secrets

Add these secrets to your GitHub repository:

1. Go to Repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### Pipeline Workflow

The CI/CD pipeline automatically:

1. **Tests** on every push and pull request
   - Backend: pytest
   - Frontend: npm build

2. **Builds** on main branch push
   - Backend Docker image
   - Frontend Docker image

3. **Publishes** to Docker Hub
   - Tags: `latest` and commit SHA
   - Image names:
     - `DOCKERHUB_USERNAME/fitbook-backend`
     - `DOCKERHUB_USERNAME/fitbook-frontend`

4. **Updates** Kubernetes manifests
   - Replaces image tags with latest commit SHA
   - Commits changes with `[skip ci]` to prevent infinite loops

5. **Argo CD** detects changes
   - Automatically pulls updated manifests
   - Deploys new version to Kubernetes

## ☸️ Kubernetes Deployment

### Prerequisites

- Minikube installed
- kubectl installed
- Docker

### Setup Steps

1. **Start Minikube**
   ```bash
   minikube start
   minikube addons enable ingress
   ```

2. **Configure local hosts**
   
   Add to your hosts file:
   - **Windows**: `C:\Windows\System32\drivers\etc\hosts`
   - **Linux/Mac**: `/etc/hosts`
   
   Add the line:
   ```
   127.0.0.1 fitbook.local
   ```

3. **Deploy application**
   ```bash
   kubectl apply -f kubernetes/
   ```

4. **Verify deployment**
   ```bash
   # Check pods
   kubectl get pods -n fitbook
   
   # Check services
   kubectl get services -n fitbook
   
   # Check ingress
   kubectl get ingress -n fitbook
   
   # Get Minikube IP
   minikube ip
   ```

5. **Access application**
   
   Get the Minikube IP:
   ```bash
   minikube ip
   ```
   
   Then update your hosts file to map `fitbook.local` to the Minikube IP, or access via:
   ```
   http://MINIKUBE_IP
   ```

6. **View logs**
   ```bash
   # Backend logs
   kubectl logs -n fitbook deployment/backend -f
   
   # Frontend logs
   kubectl logs -n fitbook deployment/frontend -f
   
   # Database logs
   kubectl logs -n fitbook statefulset/postgres -f
   ```

7. **Port-forward for development**
   ```bash
   # Access backend on localhost:8000
   kubectl port-forward -n fitbook svc/backend-service 8000:8000
   
   # Access frontend on localhost:3000
   kubectl port-forward -n fitbook svc/frontend-service 3000:80
   ```

## 🔄 Argo CD Setup

### Prerequisites

- Kubernetes cluster with kubectl access
- Helm or direct kubectl

### Installation & Setup

1. **Install Argo CD**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

2. **Access Argo CD UI**
   ```bash
   kubectl -n argocd port-forward svc/argocd-server 8080:443
   ```
   
   Open: http://localhost:8080
   
   Default credentials:
   - Username: `admin`
   - Password: (retrieve with) `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

3. **Deploy FitBook Application**
   ```bash
   # Update the repository URL in argocd/application.yaml
   sed -i 's|https://github.com/YOUR_USERNAME/fitbook|https://github.com/YOUR_ACTUAL_USERNAME/fitbook|g' argocd/application.yaml
   
   kubectl apply -f argocd/application.yaml
   ```

4. **Monitor Synchronization**
   ```bash
   # Watch Argo CD sync status
   kubectl get application -n argocd
   kubectl describe application fitbook -n argocd
   ```

### How Argo CD Works

1. **Continuous Deployment**
   - Argo CD monitors the `kubernetes/` folder in the GitHub repository
   - When changes are detected, it automatically syncs the Kubernetes manifests
   - Your application updates without manual kubectl commands

2. **Workflow with GitHub Actions**
   ```
   Developer push → GitHub Actions (Build & Test) → Push to Docker Hub 
   → Update k8s manifests → Commit to GitHub → Argo CD detects change 
   → Auto-sync to Kubernetes → New version live
   ```

## 🧪 Testing

### Backend Tests

Run backend tests locally:

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

Tests include:
- Health endpoint check
- Trainer retrieval
- Booking creation
- Booking cancellation and slot availability management

### Frontend Build

Build frontend for production:

```bash
cd frontend
npm install
npm run build
```

## 📊 Kubernetes Resource Management

### View Resource Usage

```bash
# Overall cluster resources
kubectl top nodes

# Pod resource usage
kubectl top pods -n fitbook

# Describe specific pod
kubectl describe pod <pod-name> -n fitbook
```

### Scale Deployments

```bash
# Scale backend to 3 replicas
kubectl scale deployment backend --replicas=3 -n fitbook

# Scale frontend to 2 replicas
kubectl scale deployment frontend --replicas=2 -n fitbook
```

## 🔍 Monitoring & Debugging

### Access Pod Shells

```bash
# Backend pod shell
kubectl exec -it -n fitbook deployment/backend -- /bin/bash

# Database pod shell
kubectl exec -it -n fitbook statefulset/postgres -- /bin/bash
```

### View Database

```bash
# Connect to database from any pod
kubectl exec -it -n fitbook statefulset/postgres -- psql -U fitbook_user -d fitbook_db

# List tables
\dt

# Exit
\q
```

## 📝 Environment Configuration

### Development (Docker Compose)
- Database host: `postgres`
- Backend port: `8000`
- Frontend port: `3000`

### Production (Kubernetes)
- Database host: `postgres-service` (within fitbook namespace)
- Backend service: `backend-service:8000`
- Frontend service: `frontend-service:80`

## 🔐 Secrets Management

### Current Setup
- Secrets stored in `kubernetes/secret.yaml`
- Example values for demonstration

### Production Best Practices
Consider using:
- **Sealed Secrets**: For Git-friendly secret encryption
- **Hashicorp Vault**: For external secret management
- **AWS Secrets Manager**: Cloud-native solution
- **Azure Key Vault**: For Azure deployments

## 🚢 Cleanup

### Docker Compose
```bash
docker compose down -v  # -v removes volumes
```

### Kubernetes
```bash
# Delete the entire namespace (removes all resources)
kubectl delete namespace fitbook

# Or delete specific resources
kubectl delete -f kubernetes/
```

### Minikube
```bash
# Stop Minikube
minikube stop

# Delete Minikube
minikube delete
```

## 📚 Learning Resources

- **Kubernetes**: https://kubernetes.io/docs/
- **Docker**: https://docs.docker.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Argo CD**: https://argo-cd.readthedocs.io/
- **GitHub Actions**: https://docs.github.com/en/actions

## 🤝 Contributing

1. For production deployment, implement Secret encryption
2. Add monitoring with Prometheus/Grafana
3. Implement logging with ELK or similar
4. Add automated backup strategies for PostgreSQL
5. Implement rate limiting for API endpoints

## 📄 License

This project is for educational purposes as part of a DevOps student course.

## 👨‍💻 Author

Created for student DevOps projects.

## ❓ Troubleshooting

### Frontend can't connect to backend
- Check if backend pod is running: `kubectl get pods -n fitbook`
- Verify service: `kubectl get svc -n fitbook`
- Check ingress configuration: `kubectl get ingress -n fitbook`

### Database connection errors
- Verify Secret has correct credentials: `kubectl get secret fitbook-secret -n fitbook -o yaml`
- Check PostgreSQL pod logs: `kubectl logs -n fitbook statefulset/postgres`
- Ensure StatefulSet replicas are running: `kubectl get statefulset -n fitbook`

### Argo CD not syncing
- Check Application status: `kubectl describe application fitbook -n argocd`
- Verify repository access and branch
- Check Argo CD logs: `kubectl logs -n argocd deployment/argocd-application-controller`

---

**Happy Learning! 🎓**

