# GitHub Actions CI/CD Setup Guide

## Overview

This guide explains how to set up the GitHub Actions CI/CD pipeline for FitBook.

## Prerequisites

- GitHub account with repository access
- Docker Hub account
- Git installed locally

## Step 1: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `fitbook`
3. Make it **Public** (so you can use free GitHub Actions)
4. Initialize with README (optional)
5. Create repository

## Step 2: Clone and Push Code

```bash
# Clone your new repository
git clone https://github.com/YOUR_USERNAME/fitbook.git
cd fitbook

# Copy all FitBook files into this directory
# (frontend, backend, kubernetes, etc.)

# Initialize git (if not already done)
git add .
git commit -m "Initial commit: FitBook project structure"
git push origin main
```

## Step 3: Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com)
2. Sign in to your account
3. Click on your profile → **Account Settings**
4. Left sidebar → **Security**
5. Click **New Access Token**
   - Token name: `github-actions-fitbook`
   - Permissions: Read & Write, Delete
   - Click **Generate**
6. Copy the token (you'll only see it once!)

## Step 4: Add GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → **Actions**
3. Click **New repository secret**

Add these two secrets:

### Secret 1: DOCKERHUB_USERNAME
- **Name**: `DOCKERHUB_USERNAME`
- **Value**: Your Docker Hub username
- Click **Add secret**

### Secret 2: DOCKERHUB_TOKEN
- **Name**: `DOCKERHUB_TOKEN`
- **Value**: The token you copied from Docker Hub
- Click **Add secret**

## Step 5: Verify Workflow File

Check that `.github/workflows/ci-cd.yml` exists in your repository:

```bash
# From repository root
ls -la .github/workflows/
```

## Step 6: Test the Pipeline

1. Make a small change to any file
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```

3. Go to **Actions** tab in GitHub
4. Watch the workflow run
5. Check logs for any errors

## Pipeline Stages Explained

### Stage 1: Test Backend

```
- Checks out code
- Installs Python 3.11
- Installs requirements.txt
- Runs: pytest test_main.py
```

**Success Criteria**:
- All tests pass
- No import errors
- No dependency conflicts

### Stage 2: Test Frontend

```
- Checks out code
- Sets up Node.js 20
- Installs npm dependencies
- Runs: npm run build
```

**Success Criteria**:
- Build completes successfully
- No compilation errors
- No TypeScript issues

### Stage 3: Build and Push (Main Branch Only)

```
Only runs if:
- Previous tests passed
- Push is to main branch
- Event is push (not pull request)

Actions:
1. Build backend Docker image
2. Build frontend Docker image
3. Login to Docker Hub
4. Push backends image with:
   - Tag: latest
   - Tag: commit SHA (e.g., abc12345)
5. Push frontend image with same tags
6. Update Kubernetes manifests with new SHA
7. Commit changes with [skip ci] flag
8. Push updated manifests
```

## Environment Variables

The pipeline uses these variables:

```yaml
REGISTRY: docker.io          # Docker Hub
BACKEND_IMAGE_NAME: fitbook-backend
FRONTEND_IMAGE_NAME: fitbook-frontend
```

These are combined with secrets to create image names:
- `${{ secrets.DOCKERHUB_USERNAME }}/fitbook-backend:latest`
- `${{ secrets.DOCKERHUB_USERNAME }}/fitbook-backend:abc123`

## Viewing Workflow Runs

1. Go to repository → **Actions** tab
2. Click on any workflow run
3. Expand any job to see detailed logs
4. Check for errors in red text

### Common Issues

#### ❌ "docker: not found"
- Docker Buildx might not be installed
- Solution: Ensure `setup-buildx-action@v3` is in workflow

#### ❌ "401 Unauthorized"
- Docker Hub credentials are incorrect
- Solution: Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`

#### ❌ Workflow doesn't trigger
- Workflow file might have syntax errors
- Solution: Check `.github/workflows/ci-cd.yml` for valid YAML

#### ❌ Tests fail
- Backend tests require database
- Solution: Tests use in-memory SQLite, should not need PostgreSQL
- Check test file has proper imports

## Pushing Images Manually

For testing/manual deployments:

```bash
# Build backend
docker build -t YOUR_USERNAME/fitbook-backend:manual ./backend

# Build frontend
docker build -t YOUR_USERNAME/fitbook-frontend:manual ./frontend

# Login to Docker Hub
docker login

# Push
docker push YOUR_USERNAME/fitbook-backend:manual
docker push YOUR_USERNAME/fitbook-frontend:manual
```

## Viewing Docker Hub Images

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign in
3. Click your username
4. You'll see repositories:
   - `fitbook-backend`
   - `fitbook-frontend`
5. Click on each to see tags and image history

## Updating Kubernetes Manifests

The pipeline automatically updates image tags in:
- `kubernetes/backend-deployment.yaml`
- `kubernetes/frontend-deployment.yaml`

These are used by Argo CD to deploy new versions.

### Manual Update Example

If you need to manually update the image tag:

```bash
# Before
image: DOCKERHUB_USERNAME/fitbook-backend:IMAGE_TAG_BACKEND

# After
image: your-username/fitbook-backend:abc12345
```

Then commit and push (Argo CD will detect the change).

## [skip ci] Flag

The CI pipeline uses `[skip ci]` in commit messages when updating Kubernetes manifests. This prevents infinite loops:

```
Push code → Tests & Build → Update manifests → Commit with [skip ci]
                                                      ↓
                                            Pipeline DOESN'T run
```

Without `[skip ci]`, the pipeline would:
1. Run and update manifests
2. Commit changes
3. Detect new commit
4. Run again... and again... (infinite loop!)

## Troubleshooting

### Workflow stuck in "Pending"
- GitHub Actions might be rate-limited
- Wait a few minutes and try again
- Check GitHub Status page

### Build takes too long
- Normal first-time build: 5-15 minutes
- Docker image pulls might be slow
- Check runner logs for download speeds

### Images not appearing in Docker Hub
- Check if you're logged in correctly
- Verify token has proper permissions
- Check Docker Hub activity log

## Next Steps

1. **Verify Pipeline Works**
   - Make a test commit
   - Watch Actions tab
   - Confirm images pushed to Docker Hub

2. **Set Up Argo CD**
   - Install on Kubernetes
   - Create Application resource
   - Point to your GitHub repository

3. **Monitor Deployments**
   - Watch Argo CD for automatic syncs
   - Verify new images deployed
   - Check Kubernetes pods

## Security Best Practices

✅ **DO**:
- Use short-lived tokens
- Rotate tokens regularly
- Use separate tokens for different services
- Never commit secrets to Git
- Use `[skip ci]` to prevent loops

❌ **DON'T**:
- Commit Docker Hub tokens
- Use admin-level permissions
- Hardcode credentials in code
- Share token with others
- Use same token for multiple services

## Advanced Configuration

### Change Trigger Conditions

Edit `.github/workflows/ci-cd.yml`:

```yaml
# Run on every push
on: [push]

# Run on specific branches
on:
  push:
    branches: [ main, develop, staging ]

# Run on schedule
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly at midnight Sunday
```

### Add Slack Notifications

Add to workflow:

```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'FitBook build failed'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Code Quality Scanning

```yaml
- name: Run SonarQube
  uses: sonarsource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

---

**Last Updated**: June 2024

