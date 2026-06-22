# Argo CD GitOps Deployment Guide

## Overview

Argo CD enables continuous deployment by monitoring your GitHub repository and automatically syncing Kubernetes manifests. This implements GitOps principles where Git is the single source of truth.

## Prerequisites

- Kubernetes cluster (Minikube or online)
- kubectl installed and configured
- Helm (optional, but recommended)
- Git repository with Kubernetes manifests

## Installation

### Option 1: Using kubectl (Direct)

```bash
# Create argocd namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for deployment
kubectl wait --for=condition=available \
  --timeout=300s deployment/argocd-server -n argocd

# Verify installation
kubectl get pods -n argocd
```

### Option 2: Using Helm

```bash
# Add Argo CD Helm repository
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install Argo CD
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --values argocd-values.yaml

# Verify
kubectl get pods -n argocd
```

## Initial Setup

### Step 1: Access Argo CD UI

```bash
# Port-forward to the Argo CD server
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Open browser
# https://localhost:8080
```

### Step 2: Get Initial Credentials

```bash
# Get admin password
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d)

echo "Username: admin"
echo "Password: $ARGOCD_PASSWORD"
```

**Login:**
- Username: `admin`
- Password: (from above)

### Step 3: Change Admin Password

Inside Argo CD UI:

1. Click on **Settings** (gear icon)
2. Go to **Accounts**
3. Click on **admin**
4. Set new password
5. Or use CLI:

```bash
# Change password via CLI
argocd login localhost:8080 --username admin --password "$ARGOCD_PASSWORD"
argocd account update-password --account admin --new-password "new-password"
```

## Deploy FitBook Application

### Step 1: Create GitHub Personal Access Token

If using private repository:

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click **Generate new token (classic)**
3. Name: `argocd-fitbook`
4. Select scopes: `repo` (full control)
5. Generate token
6. Copy token (won't be shown again)

### Step 2: Add Repository to Argo CD

```bash
# Via CLI
argocd repo add https://github.com/YOUR_USERNAME/fitbook \
  --username YOUR_USERNAME \
  --password YOUR_GITHUB_TOKEN

# Verify
argocd repo list
```

Or via UI:
1. Settings → Repositories
2. Click Connect Repo
3. Fill in details
4. Click Connect

### Step 3: Create Application Resource

```bash
# Update the repository URL in argocd/application.yaml
sed -i 's|https://github.com/YOUR_USERNAME/fitbook|https://github.com/YOUR_ACTUAL_USERNAME/fitbook|g' \
  argocd/application.yaml

# Deploy the Application resource
kubectl apply -f argocd/application.yaml
```

**application.yaml breakdown:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fitbook
  namespace: argocd
spec:
  # Which project (default for this example)
  project: default
  
  # Source: where to sync from (GitHub)
  source:
    repoURL: https://github.com/YOUR_USERNAME/fitbook
    targetRevision: main              # Branch to track
    path: kubernetes                  # Path to manifests
  
  # Destination: where to sync to (local Kubernetes)
  destination:
    server: https://kubernetes.default.svc
    namespace: fitbook
  
  # Sync policy: how to synchronize
  syncPolicy:
    automated:
      prune: true      # Delete resources not in Git
      selfHeal: true   # Auto-sync when cluster diverges
    syncOptions:
    - CreateNamespace=true  # Create namespace if missing
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Step 4: Verify Application Creation

```bash
# Via CLI
argocd app list
argocd app get fitbook

# Via kubectl
kubectl get application -n argocd
kubectl describe application fitbook -n argocd

# Via UI
# Applications → fitbook
```

## Workflow: CI/CD → Argo CD

### Complete Flow

```
1. Developer pushes code to GitHub
         ↓
2. GitHub Actions workflow triggers:
   - Run tests
   - Build Docker images
   - Push to Docker Hub
         ↓
3. GitHub Actions updates Kubernetes manifests:
   - Replace image tags with commit SHA
   - Commit with [skip ci] flag
   - Push to GitHub
         ↓
4. Argo CD detects repository changes:
   - Polls every 3 minutes (default)
   - Or receives webhook notification
         ↓
5. Argo CD creates/updates Application resource:
   - Compares desired (Git) vs actual (Kubernetes)
         ↓
6. Argo CD syncs to Kubernetes:
   - Updates Deployments with new images
   - Kubernetes creates new pods
   - Old pods are terminated
         ↓
7. Application running with new version ✓
```

### Setup Webhook (Optional - Faster Sync)

```bash
# Get webhook URL
WEBHOOK_URL=$(argocd app get fitbook -o jsonpath='{.status.repoStatus.webHookRequestURL}')
echo $WEBHOOK_URL
```

In GitHub repository:
1. Settings → Webhooks
2. Add webhook
3. Payload URL: (from above)
4. Content type: application/json
5. Trigger: Push events
6. Add webhook

Now Argo CD syncs immediately on push (no 3-minute delay).

## Monitoring Synchronization

### CLI Commands

```bash
# Get application status
argocd app get fitbook

# Watch for changes
argocd app wait fitbook --timeout 300

# Get detailed status
kubectl describe application fitbook -n argocd

# View sync status
kubectl get application fitbook -n argocd -o yaml | grep -A 10 "status:"
```

### Expected Output

```
Name:               fitbook
Namespace:          argocd
Status:             Synced
Health Status:      Healthy

Sync Status:        Synced (to main)
Last Full Sync:     2024-06-23T10:30:45Z

Resources:
  NAME                                           STATUS    HEALTH
  apps/Deployment/fitbook/backend                Synced    Healthy
  apps/Deployment/fitbook/frontend               Synced    Healthy
  apps/Service/fitbook/backend-service           Synced    Healthy
  apps/Service/fitbook/frontend-service          Synced    Healthy
  apps/StatefulSet/fitbook/postgres              Synced    Healthy
  v1/ConfigMap/fitbook/fitbook-config            Synced    Healthy
  v1/Secret/fitbook/fitbook-secret               Synced    Healthy
```

## Manual Sync

If you need to sync manually (without waiting for auto-sync):

```bash
# Manual sync via CLI
argocd app sync fitbook

# Specific resource
argocd app sync fitbook --resource apps:Deployment:fitbook:backend

# Hard sync (replace all)
argocd app sync fitbook --hard-sync
```

Or via UI: Applications → fitbook → Sync

## Troubleshooting

### Application shows "OutOfSync"

```bash
# Check what's different
argocd app diff fitbook

# Reasons:
# 1. Manual changes in Kubernetes (should not do this!)
# 2. Image tag updated but manifest not committed
# 3. One of the resources failed to sync

# Solution: Sync again
argocd app sync fitbook
```

### Health shows "Degraded"

```bash
# Check pod status
kubectl get pods -n fitbook

# Check pod logs
kubectl logs -n fitbook deployment/backend -f

# Check events
kubectl get events -n fitbook --sort-by='.lastTimestamp'
```

**Common issues:**
- Image not found in Docker Hub
- Database connection failed
- Resource constraints

### Sync keeps failing

```bash
# View sync errors
argocd app get fitbook --refresh

# Check Argo CD controller logs
kubectl logs -n argocd deployment/argocd-application-controller -f

# Check repository connection
argocd repo get https://github.com/YOUR_USERNAME/fitbook
```

### Cannot connect to repository

```bash
# Verify credentials
argocd repo list

# Test connection
argocd repo get https://github.com/YOUR_USERNAME/fitbook

# If private repo:
# - Check GitHub token not expired
# - Verify token has 'repo' scope
# - Re-add repository with correct credentials
```

## Advanced Features

### Sync Strategies

#### PreSync Hooks (Before Sync)

Run scripts before application deployment (e.g., database migrations):

```yaml
spec:
  syncPolicy:
    syncOptions:
    - Exec=true
  project: default
  source:
    repoURL: https://github.com/YOUR_USERNAME/fitbook
    path: kubernetes
```

Add to manifests:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-phase: PreSync
```

#### PostSync Hooks

Run after successful sync (e.g., smoke tests):

```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-phase: PostSync
```

### Multiple Environments

Create different Application resources for dev/staging/production:

```yaml
# argocd/application-dev.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fitbook-dev
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/YOUR_USERNAME/fitbook
    targetRevision: develop        # Different branch
    path: kubernetes/overlays/dev   # Different manifests
  destination:
    namespace: fitbook-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

---
# argocd/application-prod.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fitbook-prod
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/YOUR_USERNAME/fitbook
    targetRevision: main
    path: kubernetes/overlays/prod
  destination:
    namespace: fitbook-prod
  syncPolicy:
    automated: false              # Manual sync only for production!
    syncOptions:
    - CreateNamespace=true
```

### Kustomize Integration

For overlay-based deployments:

```yaml
source:
  repoURL: https://github.com/YOUR_USERNAME/fitbook
  targetRevision: main
  path: kubernetes/base
  kustomize:
    images:
    - name: fitbook-backend
      newTag: v1.2.3
```

## Argo CD UI Features

### Applications Dashboard

- **Status**: Synced/OutOfSync/Unknown
- **Health**: Healthy/Degraded/Progressing
- **Sync**: Last sync time and result
- **Resources**: Tree view of all resources

### Resource Details

Click on any resource to see:
- YAML definition
- Events
- Pod logs
- Terminal access

### Settings

1. **Repositories**: Manage Git sources
2. **Clusters**: Connect additional clusters
3. **Projects**: RBAC and constraints
4. **Accounts**: User management
5. **General**: System settings

## Best Practices

### 1. **Use GitOps Principles**
- ✅ All infrastructure in Git
- ✅ Git is single source of truth
- ✅ No manual kubectl apply
- ✅ Diff before sync

### 2. **Separate Concerns**
- ✅ Different repos for dev/staging/prod
- ✅ Or different branches (main/develop)
- ✅ Or different paths (kubernetes/overlays)

### 3. **RBAC & Security**
- ✅ Use multiple projects with RBAC
- ✅ Limit who can sync to production
- ✅ Audit all changes
- ✅ Use pull request reviews before merge

### 4. **Monitoring**
- ✅ Monitor sync status
- ✅ Set up notifications (Slack, email)
- ✅ Track health metrics
- ✅ Alert on failed syncs

### 5. **Testing**
- ✅ Test manifests in Git before merge
- ✅ Use kustomize/helm for validation
- ✅ Automated policy checks
- ✅ Manual review for production changes

## Notifications (Slack Example)

Add Slack integration to Argo CD:

```bash
# Edit argocd-notifications-cm ConfigMap
kubectl edit configmap argocd-notifications-cm -n argocd
```

Add:
```yaml
service.slack: |
  token: $slack-token

template.app-deployed: |
  message: |
    Application {{.app.metadata.name}} sync is {{.app.status.operationState.phase}}.
  slack:
    attachments: |
      [{
        "color": "#18be52",
        "fields": [
          {
            "title": "Sync Status",
            "value": "{{.app.status.operationState.phase}}",
            "short": true
          }
        ]
      }]

trigger.on-deployed: |
  - when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
    oncePer: app.status.operation.finishedAt
    send: [app-deployed]
```

Store Slack token:
```bash
kubectl create secret generic slack-token \
  --from-literal=slack-token="xoxb-YOUR-TOKEN" \
  -n argocd
```

## Cleanup & Uninstall

### Delete Application

```bash
# This removes the Application resource but not the deployed apps
argocd app delete fitbook --cascade=foreground

# Or let Kubernetes clean up resources
argocd app delete fitbook --cascade=background
```

### Uninstall Argo CD

```bash
# Delete namespace (removes all Argo CD components)
kubectl delete namespace argocd

# Or selective deletion
kubectl delete -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Learning Resources

- **Argo CD Docs**: https://argo-cd.readthedocs.io/
- **GitOps Guide**: https://www.weave.works/technologies/gitops/
- **Kustomize**: https://kustomize.io/
- **Helm**: https://helm.sh/

---

**Last Updated**: June 2024

