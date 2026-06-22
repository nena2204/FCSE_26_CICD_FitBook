# FitBook - Quick Reference Guide

## 🚀 Quick Start Commands

### Local Development (Docker Compose)

```bash
# Navigate to project
cd fitbook

# Start all services
docker compose up --build

# Stop services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v

# View logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Access services
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
```

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_main.py -v

# Start server manually
uvicorn main:app --reload

# Initialize sample data
python init_sample_data.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## ☸️ Kubernetes (Minikube) Commands

### Cluster Setup

```bash
# Start Minikube
minikube start --cpus 4 --memory 4096

# Enable Ingress
minikube addons enable ingress

# Get Minikube IP
minikube ip

# Open dashboard
minikube dashboard

# Stop Minikube
minikube stop

# Delete Minikube
minikube delete
```

### Deployment

```bash
# Deploy all manifests
kubectl apply -f kubernetes/

# Deploy specific file
kubectl apply -f kubernetes/backend-deployment.yaml

# Delete namespace (removes all resources)
kubectl delete namespace fitbook

# View all resources
kubectl get all -n fitbook
```

### Pods & Services

```bash
# List pods
kubectl get pods -n fitbook

# Watch pods
kubectl get pods -n fitbook -w

# Pod details
kubectl describe pod <pod-name> -n fitbook

# List services
kubectl get svc -n fitbook

# List ingress
kubectl get ingress -n fitbook
```

### Logs & Debugging

```bash
# View logs
kubectl logs deployment/backend -n fitbook

# Follow logs
kubectl logs deployment/backend -n fitbook -f

# Previous logs (if pod crashed)
kubectl logs deployment/backend -n fitbook --previous

# Shell access
kubectl exec -it deployment/backend -n fitbook -- /bin/bash

# Check events
kubectl get events -n fitbook --sort-by='.lastTimestamp'
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment backend --replicas=3 -n fitbook

# View replicas
kubectl get deployment backend -n fitbook

# Autoscaling
kubectl autoscale deployment backend --min=2 --max=5 --cpu-percent=80 -n fitbook
```

### Port Forwarding

```bash
# Forward frontend to localhost:3000
kubectl port-forward svc/frontend-service 3000:80 -n fitbook &

# Forward backend to localhost:8000
kubectl port-forward svc/backend-service 8000:8000 -n fitbook &

# Forward database to localhost:5432
kubectl port-forward statefulset/postgres 5432:5432 -n fitbook &
```

### Database Access

```bash
# Connect to PostgreSQL
kubectl exec -it statefulset/postgres -n fitbook -- \
  psql -U fitbook_user -d fitbook_db

# Inside psql:
\dt               # List tables
\d trainers       # Describe table
SELECT * FROM trainers;  # Query data
\q               # Exit
```

## 🔄 Argo CD Commands

```bash
# List applications
argocd app list

# Get application details
argocd app get fitbook

# Check sync status
argocd app wait fitbook

# Manual sync
argocd app sync fitbook

# Diff current vs deployed
argocd app diff fitbook

# Monitor with watch
argocd app get fitbook --refresh
```

## 📦 Docker Commands

### Building Images

```bash
# Build backend image
docker build -t your-username/fitbook-backend ./backend

# Build frontend image
docker build -t your-username/fitbook-frontend ./frontend

# Run container
docker run -p 8000:8000 your-username/fitbook-backend

# View images
docker images | grep fitbook
```

### Docker Hub

```bash
# Login to Docker Hub
docker login

# Push image
docker push your-username/fitbook-backend

# Pull image
docker pull your-username/fitbook-backend

# View image details
docker inspect your-username/fitbook-backend
```

## 🔧 GitHub Actions

### Trigger Workflow

```bash
# Make a change and push to main
git add .
git commit -m "Update: trigger CI/CD"
git push origin main

# Or create a tag
git tag v1.0.0
git push origin v1.0.0
```

### View Workflow Result

1. Go to repository → Actions tab
2. Click on the workflow run
3. Expand each job to view logs

## 📝 Common Workflows

### Deploy Local Changes

```bash
# 1. Start Minikube
minikube start --cpus 4 --memory 4096
minikube addons enable ingress

# 2. Update hosts file
MINIKUBE_IP=$(minikube ip)
# Add to /etc/hosts (or Windows equivalent):
# $MINIKUBE_IP fitbook.local

# 3. Update image in kubernetes manifests
sed -i 's/DOCKERHUB_USERNAME/your-username/g' kubernetes/*.yaml

# 4. Deploy
kubectl apply -f kubernetes/

# 5. Access application
# http://fitbook.local
```

### Update After Code Push

```bash
# 1. Push code to GitHub
git add .
git commit -m "Update: new feature"
git push origin main

# 2. GitHub Actions automatically:
#    - Runs tests
#    - Builds images
#    - Pushes to Docker Hub
#    - Updates manifests

# 3. Argo CD automatically:
#    - Detects changes
#    - Syncs to Kubernetes

# 4. Check deployment
kubectl get deployment backend -n fitbook
kubectl logs deployment/backend -n fitbook -f
```

### Rollback to Previous Version

```bash
# View deployment history
kubectl rollout history deployment/backend -n fitbook

# Rollback to previous
kubectl rollout undo deployment/backend -n fitbook

# Or specify revision
kubectl rollout undo deployment/backend --to-revision=2 -n fitbook

# Check rollout status
kubectl rollout status deployment/backend -n fitbook
```

## 🐛 Troubleshooting

### Pod won't start

```bash
# Check pod status
kubectl describe pod <pod-name> -n fitbook

# Check recent logs
kubectl logs pod/<pod-name> -n fitbook

# Check events
kubectl get events -n fitbook --sort-by='.lastTimestamp'

# Common fixes:
# - Wrong image name: kubectl set image deployment/backend backend=correct-image
# - Not enough resources: kubectl describe node
# - Database not ready: kubectl logs statefulset/postgres -n fitbook
```

### Can't access application

```bash
# Check ingress
kubectl get ingress -n fitbook
kubectl describe ingress fitbook-ingress -n fitbook

# Check frontend pod
kubectl logs deployment/frontend -n fitbook

# Check backend pod
kubectl logs deployment/backend -n fitbook

# Test connectivity from pod
kubectl exec pod/<backend-pod> -n fitbook -- \
  curl postgres-service:5432
```

### Database connection error

```bash
# Check if postgres is running
kubectl get statefulset postgres -n fitbook

# Check logs
kubectl logs statefulset/postgres -n fitbook

# Check credentials
kubectl get secret fitbook-secret -n fitbook -o yaml

# Connect directly
kubectl exec -it statefulset/postgres -n fitbook -- \
  psql -U fitbook_user -d fitbook_db -c "SELECT 1;"
```

## 📊 Useful Information

### Default Credentials

```
Database User: fitbook_user
Database Password: fitbook_password
Database Name: fitbook_db
Database Host: postgres (Docker Compose) / postgres-service (K8s)
Database Port: 5432
```

### Service Endpoints

```
Docker Compose:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432

Kubernetes (Local):
- Frontend: http://fitbook.local (or http://MINIKUBE_IP)
- Backend: http://fitbook.local/api (via ingress)
- Database: Not directly accessible (internal only)

Kubernetes (Port-Forward):
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432
```

### Resource Limits

```
Backend Pod:
- Request: 100m CPU, 256Mi Memory
- Limit: 500m CPU, 512Mi Memory

Frontend Pod:
- Request: 50m CPU, 128Mi Memory
- Limit: 200m CPU, 256Mi Memory

PostgreSQL Pod:
- Request: 100m CPU, 256Mi Memory
- Limit: 500m CPU, 512Mi Memory
```

## 🔗 Quick Links

- **GitHub Repository**: https://github.com/YOUR_USERNAME/fitbook
- **Docker Hub**: https://hub.docker.com/u/YOUR_USERNAME
- **Local Frontend**: http://localhost:3000
- **Local Backend**: http://localhost:8000
- **Local Kubernetes**: http://fitbook.local
- **Argo CD UI**: https://localhost:8080

## 📚 Documentation

- [README.md](../README.md) - Project overview
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [CI-CD-SETUP.md](./CI-CD-SETUP.md) - GitHub Actions
- [KUBERNETES-DEPLOYMENT.md](./KUBERNETES-DEPLOYMENT.md) - Kubernetes guide
- [ARGOCD-SETUP.md](./ARGOCD-SETUP.md) - Argo CD guide
- [DEPLOYMENT-CHECKLIST.md](../DEPLOYMENT-CHECKLIST.md) - Full checklist

## ⚡ Pro Tips

1. **Use aliases for common commands**
   ```bash
   alias kgp='kubectl get pods -n fitbook'
   alias kl='kubectl logs -n fitbook'
   ```

2. **Auto-complete kubectl**
   ```bash
   source <(kubectl completion bash)
   ```

3. **Monitor resources in real-time**
   ```bash
   kubectl top pods -n fitbook
   ```

4. **Watch changes live**
   ```bash
   kubectl get pods -n fitbook -w
   ```

5. **Use multi-line commands in shell profile**
   ```bash
   # Add to ~/.bash_profile or ~/.zshrc
   function minikube-demo {
     minikube start --cpus 4 --memory 4096
     minikube addons enable ingress
     kubectl apply -f kubernetes/
   }
   ```

---

**Last Updated**: June 2024

**Need Help?** Check the full documentation in the `docs/` folder.

