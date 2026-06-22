# Kubernetes Deployment Guide

## Prerequisites

Before starting, ensure you have:

```bash
# Check installations
minikube version
kubectl version --client
docker --version
git --version
```

## Quick Start (Copy-Paste Commands)

```bash
# 1. Start Minikube
minikube start --cpus 4 --memory 4096

# 2. Enable Ingress
minikube addons enable ingress

# 3. Clone and navigate to repo
git clone https://github.com/YOUR_USERNAME/fitbook.git
cd fitbook

# 4. Deploy FitBook
kubectl apply -f kubernetes/

# 5. Check deployment
kubectl get pods -n fitbook
kubectl get services -n fitbook
kubectl get ingress -n fitbook

# 6. Access the app
minikube ip  # Note this IP
# Update hosts file with this IP: fitbook.local
# Open http://fitbook.local in browser

# 7. View logs
kubectl logs -n fitbook deployment/backend -f
```

## Detailed Setup

### Step 1: Start Minikube

```bash
# Basic start
minikube start

# With more resources (recommended)
minikube start \
  --cpus 4 \
  --memory 4096 \
  --disk-size 20000mb

# With specific container runtime
minikube start --container-runtime=docker

# With hypervisor
minikube start --driver=virtualbox  # or hyperv, vmware, etc.
```

**Verify:**
```bash
minikube status
kubectl cluster-info
```

### Step 2: Enable Ingress

```bash
# Enable NGINX Ingress addon
minikube addons enable ingress

# Verify
kubectl get ns
kubectl get pods -n ingress-nginx
```

### Step 3: Configure Local Hosts File

Find Minikube IP:
```bash
MINIKUBE_IP=$(minikube ip)
echo $MINIKUBE_IP
```

#### Windows (Admin required)

1. Open Notepad as Administrator
2. Open file: `C:\Windows\System32\drivers\etc\hosts`
3. Add line at end: `MINIKUBE_IP fitbook.local`
   - Replace `MINIKUBE_IP` with actual IP from command above
4. Save file

Example:
```
192.168.99.100 fitbook.local
```

#### macOS/Linux

```bash
MINIKUBE_IP=$(minikube ip)

# Add to hosts file
echo "$MINIKUBE_IP fitbook.local" | sudo tee -a /etc/hosts

# Verify
cat /etc/hosts | grep fitbook
```

### Step 4: Update Kubernetes Manifests

Edit image placeholders with your Docker Hub username:

```bash
# Replace DOCKERHUB_USERNAME with your actual username
sed -i 's/DOCKERHUB_USERNAME/your-docker-username/g' kubernetes/*.yaml

# Or manually edit:
# kubernetes/backend-deployment.yaml
# kubernetes/frontend-deployment.yaml
```

### Step 5: Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Or apply individually
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/postgres-statefulset.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### Step 6: Verify Deployment

```bash
# Check namespace creation
kubectl get ns

# Check all resources in fitbook namespace
kubectl get all -n fitbook

# Check specific resources
kubectl get pods -n fitbook
kubectl get svc -n fitbook
kubectl get deploy -n fitbook
kubectl get statefulset -n fitbook
kubectl get ingress -n fitbook
kubectl get pvc -n fitbook
```

### Step 7: Wait for Services to Be Ready

```bash
# Watch pod status (Ctrl+C to exit)
kubectl get pods -n fitbook -w

# Expected output eventually:
# NAME                        READY   STATUS    RESTARTS
# backend-xxxxx               1/1     Running   0
# backend-xxxxx               1/1     Running   0
# frontend-xxxxx              1/1     Running   0
# postgres-0                  1/1     Running   0
```

### Step 8: Access the Application

```bash
# Get Minikube IP
minikube ip

# Open in browser:
# http://fitbook.local
# http://fitbook.local/api/docs (API documentation)

# Or use port-forward (alternative)
kubectl port-forward -n fitbook svc/frontend-service 8080:80
# Then open: http://localhost:8080
```

## Common Kubernetes Commands

### View Resources

```bash
# Pods
kubectl get pods -n fitbook
kubectl describe pod <pod-name> -n fitbook
kubectl logs pod/<pod-name> -n fitbook

# Services
kubectl get svc -n fitbook
kubectl describe svc backend-service -n fitbook

# Deployments
kubectl get deploy -n fitbook
kubectl describe deploy backend -n fitbook
kubectl scale deploy backend --replicas=3 -n fitbook

# StatefulSets
kubectl get statefulset -n fitbook
kubectl describe statefulset postgres -n fitbook

# Ingress
kubectl get ingress -n fitbook
kubectl describe ingress fitbook-ingress -n fitbook

# ConfigMaps & Secrets
kubectl get configmap -n fitbook
kubectl get secret -n fitbook
kubectl describe configmap fitbook-config -n fitbook
```

### View Logs

```bash
# Single pod
kubectl logs pod/backend-xxxxx -n fitbook

# All pods in deployment
kubectl logs deployment/backend -n fitbook

# Follow logs (tail -f)
kubectl logs deployment/backend -n fitbook -f

# Last 100 lines
kubectl logs deployment/backend -n fitbook --tail=100

# All containers
kubectl logs pod/postgres-0 -n fitbook --all-containers=true
```

### Execute Commands in Pods

```bash
# Interactive shell
kubectl exec -it pod/backend-xxxxx -n fitbook -- /bin/bash

# Run command
kubectl exec pod/postgres-0 -n fitbook -- psql -U fitbook_user -d fitbook_db

# List environment variables
kubectl exec pod/backend-xxxxx -n fitbook -- env
```

### Port Forwarding

```bash
# Forward frontend
kubectl port-forward -n fitbook svc/frontend-service 3000:80 &

# Forward backend
kubectl port-forward -n fitbook svc/backend-service 8000:8000 &

# Forward database
kubectl port-forward -n fitbook statefulset/postgres 5432:5432 &

# Kill port-forward
# Windows: taskkill /F /IM kubectl.exe
# Linux/Mac: pkill -f port-forward
```

### Debugging

```bash
# Check events
kubectl get events -n fitbook --sort-by='.lastTimestamp'

# Describe resource in detail
kubectl describe pod <pod-name> -n fitbook

# Get resource definition
kubectl get pod <pod-name> -n fitbook -o yaml

# Resource usage
kubectl top nodes
kubectl top pods -n fitbook
```

## Database Operations

### Connect to PostgreSQL

```bash
# Using exec
kubectl exec -it -n fitbook statefulset/postgres -- \
  psql -U fitbook_user -d fitbook_db

# Once inside psql:
\dt              # List tables
SELECT * FROM trainers;  # View data
\d trainers      # Describe table
\q              # Exit
```

### Backup Database

```bash
# Create backup
kubectl exec -n fitbook statefulset/postgres -- \
  pg_dump -U fitbook_user fitbook_db > fitbook_backup.sql

# Restore backup
kubectl exec -i -n fitbook statefulset/postgres -- \
  psql -U fitbook_user fitbook_db < fitbook_backup.sql
```

### View Database Storage

```bash
# List PersistentVolumes
kubectl get pv

# List PersistentVolumeClaims
kubectl get pvc -n fitbook

# Check storage usage
kubectl describe pvc postgres-storage-postgres-0 -n fitbook
```

## Scaling Applications

### Scale Backend

```bash
# Scale to 3 replicas
kubectl scale deployment backend --replicas=3 -n fitbook

# Verify
kubectl get pods -n fitbook -l app=backend
```

### Scale Frontend

```bash
# Scale to 2 replicas
kubectl scale deployment frontend --replicas=2 -n fitbook

# Verify
kubectl get pods -n fitbook -l app=frontend
```

### Set Autoscaling (Advanced)

```bash
# Create HPA (Horizontal Pod Autoscaler)
kubectl autoscale deployment backend \
  --min=2 --max=5 \
  --cpu-percent=80 \
  -n fitbook

# Check HPA status
kubectl get hpa -n fitbook
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n fitbook

# Common issues in "Events" section:
# - ImagePullBackOff: Wrong image name/tag
# - CrashLoopBackOff: Application crash
# - Pending: Resource constraints
```

**Solutions:**

```bash
# Wrong image? Update it
kubectl set image deployment/backend \
  backend=your-username/fitbook-backend:latest \
  -n fitbook

# Pod has no resources? Check node capacity
kubectl describe nodes
```

### Services not accessible

```bash
# Check service endpoints
kubectl get endpoints -n fitbook

# Empty? Pod might not be ready
# Check pod readiness probe logs
kubectl logs pod/<pod-name> -n fitbook

# Test connectivity from pod
kubectl exec pod/backend-xxxxx -n fitbook -- \
  nc -zv postgres-service 5432
```

### Database connection errors

```bash
# Check if database pod is running
kubectl get pods -n fitbook -l app=postgres

# Check database logs
kubectl logs statefulset/postgres -n fitbook

# Try connecting directly
kubectl exec -it statefulset/postgres -n fitbook -- \
  psql -U fitbook_user -d fitbook_db
```

### Ingress not working

```bash
# Check ingress rules
kubectl describe ingress fitbook-ingress -n fitbook

# Check if hosts file is updated
# Windows: type C:\Windows\System32\drivers\etc\hosts | findstr fitbook
# Linux/Mac: grep fitbook /etc/hosts

# Test DNS resolution
nslookup fitbook.local

# Check NGINX ingress controller
kubectl get pods -n ingress-nginx
```

## Deployment Scenarios

### Update Image (Canary Deployment)

```bash
# Method 1: Set image directly
kubectl set image deployment/backend \
  backend=your-username/fitbook-backend:v2.0.0 \
  -n fitbook

# Method 2: Edit deployment
kubectl edit deployment backend -n fitbook
# Change image in editor, save and exit
```

### Rollback Deployment

```bash
# Check rollout history
kubectl rollout history deployment/backend -n fitbook

# Rollback to previous version
kubectl rollout undo deployment/backend -n fitbook

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=2 -n fitbook
```

### Restart Pods

```bash
# Restart deployment
kubectl rollout restart deployment/backend -n fitbook

# Delete specific pod (will be recreated)
kubectl delete pod <pod-name> -n fitbook
```

## Resource Management

### Check Resource Requests/Limits

```bash
# View current resources
kubectl describe pod <pod-name> -n fitbook | grep -A 5 "Requests"

# Edit resource limits
kubectl edit deployment backend -n fitbook
# Update: resources.requests and resources.limits
```

### Monitor Usage

```bash
# Real-time CPU/Memory usage
kubectl top pods -n fitbook

# Watch over time
kubectl top pods -n fitbook --containers

# Specific pod
kubectl top pod <pod-name> -n fitbook
```

## Cleanup

### Delete Individual Resources

```bash
# Delete deployment
kubectl delete deployment backend -n fitbook

# Delete service
kubectl delete service backend-service -n fitbook

# Delete pods (will be recreated if in deployment)
kubectl delete pods --all -n fitbook
```

### Delete Entire Namespace

```bash
# Delete everything in namespace
kubectl delete namespace fitbook

# Wait for deletion
kubectl get ns
```

### Delete Minikube

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Clean up minikube config
rm -rf ~/.minikube  # Linux/Mac
rmdir %USERPROFILE%\.minikube  # Windows
```

## Advanced Topics

### Custom Domain Names

Instead of `fitbook.local`, use any domain:

1. Edit `/etc/hosts` (or Windows equivalent)
2. Add: `192.168.99.100 my-app.dev`
3. Update `ingress.yaml`:
   ```yaml
   - host: my-app.dev
   ```
4. Reapply: `kubectl apply -f kubernetes/ingress.yaml`

### TLS/SSL Certificates

For production (Minikube doesn't support TLS easily):

```yaml
# In ingress.yaml
spec:
  tls:
  - hosts:
    - fitbook.local
    secretName: fitbook-tls
```

### NetworkPolicies

Restrict traffic between pods:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: fitbook
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8000
```

## Performance Tuning

### Change Resource Limits

Edit `kubernetes/backend-deployment.yaml`:

```yaml
resources:
  requests:
    memory: "512Mi"    # Minimum
    cpu: "250m"
  limits:
    memory: "1Gi"      # Maximum
    cpu: "1000m"
```

### Adjust Replica Count

```bash
# Static
kubectl scale deployment backend --replicas=5 -n fitbook

# Dynamic (HPA)
kubectl autoscale deployment backend --min=2 --max=10 \
  --cpu-percent=70 -n fitbook
```

---

**Last Updated**: June 2024

**Need More Help?**
- Kubernetes Docs: https://kubernetes.io/docs/
- Minikube Docs: https://minikube.sigs.k8s.io/docs/
- kubectl Cheatsheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

