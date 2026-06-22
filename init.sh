#!/bin/bash

# FitBook Project Initialization Script
# This script sets up sample data and prepares for deployment

set -e

echo "🚀 FitBook Project Initialization"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git."
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created (update with your settings)${NC}"
else
    echo -e "${YELLOW}⚠ .env already exists${NC}"
fi

# Initialize backend
echo -e "${BLUE}Setting up backend...${NC}"
cd backend || exit

if [ ! -f .env ]; then
    cp .env.example .env
fi

# Create Python virtual environment (optional)
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.11+"
    exit 1
fi

echo -e "${GREEN}✓ Backend ready${NC}"
cd .. || exit

# Test Docker Compose file
echo -e "${BLUE}Validating docker-compose.yml...${NC}"
if docker compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.yml is valid${NC}"
else
    echo "❌ docker-compose.yml has errors"
    exit 1
fi

# Initialize Git (if not already)
if [ ! -d .git ]; then
    echo -e "${BLUE}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: FitBook DevOps project"
    echo -e "${GREEN}✓ Git initialized${NC}"
    echo -e "${YELLOW}⚠ Remember to: git remote add origin <your-repo-url>${NC}"
else
    echo -e "${YELLOW}⚠ Git already initialized${NC}"
fi

echo ""
echo -e "${GREEN}=================================="
echo "✓ FitBook initialized successfully!"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Update .env with your settings"
echo "2. For Docker Compose:"
echo "   docker compose up --build"
echo ""
echo "3. For Kubernetes:"
echo "   minikube start"
echo "   minikube addons enable ingress"
echo "   kubectl apply -f kubernetes/"
echo ""
echo "4. Set up GitHub Actions:"
echo "   - Create GitHub repository"
echo "   - Add DOCKERHUB_USERNAME and DOCKERHUB_TOKEN secrets"
echo "   - Push code to trigger CI/CD"
echo ""
echo "Documentation:"
echo "- README.md - Project overview"
echo "- docs/ARCHITECTURE.md - System design"
echo "- docs/CI-CD-SETUP.md - GitHub Actions setup"
echo "- docs/KUBERNETES-DEPLOYMENT.md - Kubernetes guide"
echo "- docs/ARGOCD-SETUP.md - Argo CD setup"

