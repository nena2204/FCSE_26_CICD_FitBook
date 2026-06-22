# FitBook Project - Complete Setup & Deployment Checklist

## 📋 Project Overview

**FitBook** is a complete DevOps student project demonstrating:
- ✅ Modern web application development (React + FastAPI)
- ✅ Docker containerization and Docker Compose orchestration
- ✅ GitHub Actions CI/CD pipeline
- ✅ Kubernetes deployment on Minikube
- ✅ Argo CD GitOps continuous deployment
- ✅ Production-ready security practices

## 🚀 Phase 1: Local Development Setup

### 1.1 Prerequisites Check
- [ ] Git installed: `git --version`
- [ ] Docker installed: `docker --version`
- [ ] Docker Compose installed: `docker compose --version`
- [ ] Node.js 20+ installed: `node --version`
- [ ] Python 3.11+ installed: `python --version`

### 1.2 Repository Setup
- [ ] Fork/clone repository
- [ ] Navigate to fitbook directory: `cd fitbook`
- [ ] Copy environment template: `cp .env.example .env`
- [ ] Review and update `.env` file with your settings
- [ ] Initialize git if new: `git init && git add . && git commit -m "Initial commit"`

## 🐳 Phase 2: Docker Compose Development

### 2.1 Build and Run Locally
```bash
# From fitbook root directory
docker compose up --build
```

- [ ] All three services start without errors
- [ ] Check logs for any connection issues

### 2.2 Verify Services
- [ ] Frontend accessible: http://localhost:3000
- [ ] Backend health check: http://localhost:8000/api/health
- [ ] API documentation: http://localhost:8000/docs

### 2.3 Test Application
- [ ] Navigate to Trainers page
- [ ] Check Available Slots page
- [ ] Create a booking
- [ ] View My Bookings
- [ ] Cancel a booking

### 2.4 Test Database
```bash
# Connect to PostgreSQL
docker exec -it fitbook-postgres psql -U fitbook_user -d fitbook_db

# Inside psql:
\dt              # List tables
SELECT * FROM trainers;
\q              # Exit
```

- [ ] All tables created successfully
- [ ] Data persists after compose down/up

### 2.5 Cleanup (Optional)
```bash
# Stop containers
docker compose down

# Remove volumes (deletes data)
docker compose down -v
```

## 🧪 Phase 3: Testing

### 3.1 Backend Tests
```bash
# Install dependencies (in backend directory)
cd backend
pip install -r requirements.txt

# Run tests
pytest test_main.py -v
```

- [ ] All tests pass
- [ ] Health endpoint test passes
- [ ] Trainer operations test passes
- [ ] Booking operations tests pass

### 3.2 Frontend Build
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Build production bundle
npm run build
```

- [ ] Build completes without errors
- [ ] dist/ folder created with optimized files

## 🔧 Phase 4: GitHub Repository Setup

### 4.1 Create Repository
- [ ] Create new GitHub repository named "fitbook"
- [ ] Make repository **public** (for free GitHub Actions)
- [ ] Note the repository URL

### 4.2 Push Code to GitHub
```bash
cd fitbook
git remote add origin https://github.com/YOUR_USERNAME/fitbook.git
git branch -M main
git push -u origin main
```

- [ ] Code successfully pushed to GitHub
- [ ] All files visible in web interface

### 4.3 Add GitHub Secrets

Navigate to: Repository Settings → Secrets and variables → Actions

Add these secrets:

**Secret 1: DOCKERHUB_USERNAME**
- Name: `DOCKERHUB_USERNAME`
- Value: Your Docker Hub username

**Secret 2: DOCKERHUB_TOKEN**
- Name: `DOCKERHUB_TOKEN`
- Value: Docker Hub access token

**Verification:**
```bash
# Settings → Secrets should show both secrets as registered
```

- [ ] DOCKERHUB_USERNAME secret created
- [ ] DOCKERHUB_TOKEN secret created
- [ ] Both show as "Created" in settings

### 4.4 Verify GitHub Actions Workflow
```bash
# From repository web interface
Navigate to: Actions tab

# Should see:
- ci-cd.yml workflow file
```

- [ ] Workflow file visible in Actions tab
- [ ] Ready to trigger on push

## 🚢 Phase 5: GitHub Actions CI/CD Pipeline

### 5.1 Trigger Pipeline
```bash
# Make a small change
echo "# Project initiated" >> README.md

# Commit and push
git add .
git commit -m "Trigger CI/CD pipeline"
git push origin main
```

- [ ] Workflow starts automatically
- [ ] Github Actions page shows workflow running

### 5.2 Monitor Pipeline Execution
- [ ] Navigate to repository Actions tab
- [ ] Watch "CI/CD Pipeline" workflow
- [ ] Monitor stages:
  - [ ] test-backend: ✓ Completes successfully
  - [ ] test-frontend: ✓ Builds successfully
  - [ ] build-and-push: ✓ Images pushed to Docker Hub

### 5.3 Verify Docker Images
```bash
# Login to Docker Hub and verify:
```

- [ ] `fitbook-backend:latest` image exists
- [ ] `fitbook-backend:commit-sha` image exists
- [ ] `fitbook-frontend:latest` image exists
- [ ] `fitbook-frontend:commit-sha` image exists

### 5.4 Check Updated Manifests
```bash
# Images in kubernetes manifests should be updated
cat kubernetes/backend-deployment.yaml | grep image:
cat kubernetes/frontend-deployment.yaml | grep image:
```

- [ ] Image tags updated with commit SHA
- [ ] Manifests committed with `[skip ci]` message

## ☸️ Phase 6: Kubernetes Deployment (Minikube)

### 6.1 Start Minikube
```bash
# Start with sufficient resources
minikube start --cpus 4 --memory 4096 --disk-size 20000mb

# Verify
minikube status
kubectl cluster-info
```

- [ ] Minikube cluster started
- [ ] kubectl can access cluster

### 6.2 Enable Ingress
```bash
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx
```

- [ ] Ingress controller running
- [ ] ingress-nginx pods are Ready

### 6.3 Update Kubernetes Manifests
Replace Docker Hub username in manifests:

```bash
# Update with your username
sed -i 's/DOCKERHUB_USERNAME/your-username/g' kubernetes/*.yaml

# Verify
cat kubernetes/backend-deployment.yaml | grep image:
```

- [ ] All image references updated
- [ ] No placeholder text remaining

### 6.4 Configure Hosts File

Get Minikube IP:
```bash
minikube ip  # e.g., 192.168.99.100
```

**Windows:**
1. Open Notepad as Administrator
2. Open: `C:\Windows\System32\drivers\etc\hosts`
3. Add: `192.168.99.100 fitbook.local`
4. Save

**Linux/macOS:**
```bash
echo "192.168.99.100 fitbook.local" | sudo tee -a /etc/hosts
```

- [ ] Hosts file updated with Minikube IP
- [ ] Can ping fitbook.local: `ping fitbook.local`

### 6.5 Deploy to Kubernetes
```bash
# From fitbook root directory
kubectl apply -f kubernetes/

# Verify
kubectl get pods -n fitbook
kubectl get services -n fitbook
kubectl get ingress -n fitbook
```

- [ ] All pods created and running
- [ ] All services running
- [ ] Ingress resource created

### 6.6 Wait for Services Ready
```bash
# Watch pod status (Ctrl+C to exit)
kubectl get pods -n fitbook -w

# Expected final state:
# NAME                        READY   STATUS
# backend-xxxxx               1/1     Running
# backend-xxxxx               1/1     Running
# frontend-xxxxx              1/1     Running
# postgres-0                  1/1     Running
```

- [ ] All pods in "Running" state
- [ ] All ready count shows 1/1
- [ ] No CrashLoopBackOff or pending pods

### 6.7 Test Application via Kubernetes
```bash
# Open in browser
# http://fitbook.local

# Or via port-forward
kubectl port-forward -n fitbook svc/frontend-service 8080:80
# Then: http://localhost:8080
```

- [ ] Application loads at http://fitbook.local
- [ ] Can navigate all pages
- [ ] Backend API responds to requests
- [ ] Database queries work

### 6.8 Test Database Persistence

```bash
# Check current pods
kubectl get pods -n fitbook

# Delete a backend pod (will restart automatically)
kubectl delete pod <backend-pod-name> -n fitbook

# Verify pod restarts
kubectl get pods -n fitbook -w
```

- [ ] Pod automatically restarts
- [ ] Application still functions
- [ ] Data persists

## 🔄 Phase 7: Argo CD Setup (GitOps)

### 7.1 Install Argo CD
```bash
# Create namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Verify
kubectl get pods -n argocd
```

- [ ] argocd namespace created
- [ ] All Argo CD pods running
- [ ] argocd-server pod Ready

### 7.2 Access Argo CD
```bash
# Port-forward to UI
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

- [ ] Can access https://localhost:8080
- [ ] Can login with admin credentials
- [ ] Argo CD dashboard displays

### 7.3 Add GitHub Repository
```bash
# For public repository (no auth needed)
argocd repo add https://github.com/YOUR_USERNAME/fitbook

# Verify
argocd repo list
```

- [ ] Repository added successfully
- [ ] Connection verified

### 7.4 Create Application Resource
```bash
# Update repository URL in argocd/application.yaml
sed -i 's|https://github.com/YOUR_USERNAME/fitbook|https://github.com/YOUR_ACTUAL_USERNAME/fitbook|g' argocd/application.yaml

# Deploy application
kubectl apply -f argocd/application.yaml

# Verify
argocd app list
argocd app get fitbook
```

- [ ] Application resource created
- [ ] Status shows "Synced"
- [ ] Health shows "Healthy"

### 7.5 Verify Automatic Sync
```bash
# Make a change to kubernetes manifests
echo "# Updated by Argo CD" >> kubernetes/configmap.yaml

# Commit and push
git add .
git commit -m "Test Argo CD sync"
git push

# Monitor Argo CD (should sync automatically)
argocd app get fitbook
```

- [ ] Argo CD detects changes within 3 minutes
- [ ] Application automatically syncs
- [ ] Updates reflected in Kubernetes

### 7.6 View Argo CD UI
1. Navigate to Applications tab
2. Click "fitbook"
3. View resource tree
4. Check sync status

- [ ] Application dashboard displays
- [ ] All resources shown in tree
- [ ] Healthy status maintained

## 📊 Phase 8: End-to-End Testing

### 8.1 Complete User Flow

1. **Create Data**
   - [ ] Access application at http://fitbook.local
   - [ ] Navigate to "Book Training"
   - [ ] Select a trainer and time slot
   - [ ] Create booking with name

2. **View Bookings**
   - [ ] Navigate to "My Bookings"
   - [ ] Your booking appears in list
   - [ ] Details are correct

3. **Cancel Booking**
   - [ ] Click "Cancel Booking"
   - [ ] Confirm cancellation
   - [ ] Booking removed from list
   - [ ] Slot becomes available again

### 8.2 API Testing
```bash
# Health check
curl http://localhost:8000/api/health

# Get trainers
curl http://localhost:8000/api/trainers

# Get available slots
curl http://localhost:8000/api/slots/available

# Create booking
curl -X POST http://localhost:8000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{"client_name":"John","training_slot_id":1}'

# Get bookings
curl http://localhost:8000/api/bookings
```

- [ ] All endpoints respond
- [ ] Return valid JSON
- [ ] Data is correct

### 8.3 Scale Testing
```bash
# Scale backend to 3 replicas
kubectl scale deployment backend --replicas=3 -n fitbook

# Verify
kubectl get pods -n fitbook

# Create multiple bookings
# - Should work across all replicas
```

- [ ] Multiple backend pods running
- [ ] Load distributed across replicas
- [ ] Application works correctly

## 🔐 Phase 9: Security Review

### 9.1 Secrets Management
- [ ] `.env` file in `.gitignore`
- [ ] No credentials in code
- [ ] GitHub Secrets used for CI/CD
- [ ] Kubernetes Secrets used in manifests

### 9.2 Image Security
- [ ] No hardcoded secrets in Dockerfiles
- [ ] Non-root users running containers
- [ ] Health checks implemented
- [ ] Resource limits defined

### 9.3 Network Security
- [ ] Ingress configured correctly
- [ ] Services using ClusterIP (not NodePort/LoadBalancer)
- [ ] CORS enabled only when needed
- [ ] Database only accessible internally

### 9.4 Kubernetes Security
- [ ] Namespace isolation used
- [ ] ConfigMap for non-sensitive data
- [ ] Secret for credentials
- [ ] RBAC could be implemented (future)

## 📚 Documentation Review

Review all documentation Files:

- [ ] `README.md` - Complete overview
- [ ] `docs/ARCHITECTURE.md` - System design explained
- [ ] `docs/CI-CD-SETUP.md` - GitHub Actions setup
- [ ] `docs/KUBERNETES-DEPLOYMENT.md` - K8s commands
- [ ] `docs/ARGOCD-SETUP.md` - Argo CD configuration

## 🎯 Phase 10: Presentation Preparation

### 10.1 Demo Scenarios

**Demo 1: Local Development with Docker Compose**
```bash
docker compose up --build
# Show: http://localhost:3000
# Create booking
# Check backend: http://localhost:8000/docs
```

- [ ] Scenario tested and working
- [ ] Takes ~30 seconds after build

**Demo 2: CI/CD Pipeline**
- [ ] Show GitHub repository
- [ ] Demonstrate: push code → Actions runs → Images built
- [ ] Verify images on Docker Hub

- [ ] Scenario tested
- [ ] Timing documented

**Demo 3: Kubernetes Deployment**
```bash
minikube start --cpus 4 --memory 4096
kubectl apply -f kubernetes/
# Show: http://fitbook.local
```

- [ ] Scenario tested
- [ ] Takes ~5 minutes total

**Demo 4: Argo CD Auto-Deployment**
- [ ] Make change to kubernetes manifests
- [ ] Commit and push
- [ ] Show Argo CD detecting change
- [ ] Watch automatic sync

- [ ] Scenario tested
- [ ] Takes ~3 minutes

### 10.2 Presentation Points

Key talking points for presentation:

1. **Architecture**
   - Three-tier application (Frontend/Backend/Database)
   - Each service in separate container
   - Benefits of containerization

2. **CI/CD Pipeline**
   - Automated testing on every push
   - Docker images built and published
   - GitOps approach with Argo CD

3. **Kubernetes**
   - Orchestration and deployment
   - Self-healing and scaling
   - Persistent storage with StatefulSets

4. **GitOps with Argo CD**
   - Git as single source of truth
   - Automatic synchronization
   - Easy rollbacks via Git history

- [ ] Presentation outline created
- [ ] Demo scripts tested
- [ ] Timing verified

## ✅ Final Checklist

### Project Complete When:

- [ ] Repository created on GitHub (public)
- [ ] All code pushed to main branch
- [ ] Docker Compose works locally
- [ ] All tests pass (backend and frontend)
- [ ] GitHub Actions workflow executes successfully
- [ ] Docker images pushed to Docker Hub
- [ ] Kubernetes manifests deploy successfully
- [ ] Application accessible at http://fitbook.local
- [ ] Argo CD monitors and syncs changes
- [ ] Documentation complete and clear
- [ ] One full end-to-end demo completed successfully

## 🚀 Deployment Verification

```bash
# Run this verification script to check all components

echo "=== FitBook Deployment Verification ==="
echo ""
echo "1. GitHub Repository:"
echo "   [ ] Public repository with all code"
echo ""
echo "2. Docker Compose:"
docker compose ps 2>/dev/null && echo "   [ ] Running successfully" || echo "   [ ] Not running"
echo ""
echo "3. Kubernetes (Minikube):"
kubectl get pods -n fitbook 2>/dev/null | grep Running && echo "   [ ] Pods running" || echo "   [ ] Not deployed"
echo ""
echo "4. Argo CD:"
kubectl get application -n argocd 2>/dev/null | grep fitbook && echo "   [ ] Application synced" || echo "   [ ] Not setup"
echo ""
echo "5. Docker Hub Images:"
echo "   [ ] fitbook-backend:latest"
echo "   [ ] fitbook-frontend:latest"
echo ""
echo "=== Verification Complete ==="
```

## 📞 Support & Resources

**Useful Commands:**

```bash
# Docker Compose
docker compose up --build      # Start all services
docker compose down -v          # Stop and remove volumes
docker compose logs -f          # View logs

# Kubernetes
kubectl apply -f kubernetes/    # Deploy
kubectl delete namespace fitbook # Delete all
kubectl get pods -n fitbook     # List pods
kubectl logs deployment/backend -n fitbook -f  # Logs

# Argo CD
argocd app list                 # List applications
argocd app get fitbook          # Get details
argocd app sync fitbook         # Manual sync
```

**Documentation Links:**

- Kubernetes: https://kubernetes.io/docs/
- Docker: https://docs.docker.com/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Argo CD: https://argo-cd.readthedocs.io/
- GitHub Actions: https://docs.github.com/en/actions

---

**Project Completion Date**: _______________

**Presentation Date**: _______________

**Notes/Comments**: ________________________________________________

---

**Good luck with your presentation! 🎓**

