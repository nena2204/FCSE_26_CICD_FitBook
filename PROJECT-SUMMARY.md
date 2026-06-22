# FitBook Project - Structure & Files Summary

## 📁 Complete Project Structure

```
fitbook/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICK-REFERENCE.md                 # Quick command reference
├── 📄 DEPLOYMENT-CHECKLIST.md            # Step-by-step deployment guide
├── 📄 .gitignore                         # Git ignore rules
├── 📄 .env.example                       # Environment template
├── 📄 docker-compose.yml                 # Docker Compose orchestration
├── 📄 init.sh                            # Project initialization script
│
├── 📂 backend/
│   ├── 📄 main.py                        # FastAPI application & routes
│   ├── 📄 models.py                      # SQLAlchemy database models
│   ├── 📄 schemas.py                     # Pydantic request/response schemas
│   ├── 📄 crud.py                        # Database CRUD operations
│   ├── 📄 database.py                    # Database connection & session
│   ├── 📄 config.py                      # Configuration management
│   ├── 📄 test_main.py                   # Pytest backend tests
│   ├── 📄 init_sample_data.py            # Sample data initialization
│   ├── 📄 requirements.txt                # Python dependencies
│   ├── 📄 Dockerfile                     # Backend Docker image
│   ├── 📄 pytest.ini                     # Pytest configuration
│   └── 📄 .env.example                   # Backend env template
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 pages/
│   │   │   ├── 📄 HomePage.jsx           # Home/landing page
│   │   │   ├── 📄 TrainersPage.jsx       # Trainers listing
│   │   │   ├── 📄 SlotsPage.jsx          # Available slots
│   │   │   ├── 📄 BookingPage.jsx        # Booking creation form
│   │   │   └── 📄 BookingsPage.jsx       # User bookings management
│   │   ├── 📄 App.jsx                    # Main app component with routing
│   │   ├── 📄 main.jsx                   # React entry point
│   │   └── 📄 api.js                     # Axios API client
│   ├── 📄 index.html                     # HTML template with styling
│   ├── 📄 vite.config.js                 # Vite build configuration
│   ├── 📄 package.json                   # Node.js dependencies
│   ├── 📄 Dockerfile                     # Frontend Docker image (multi-stage)
│   └── 📄 .env.example                   # Frontend env template
│
├── 📂 kubernetes/
│   ├── 📄 namespace.yaml                 # Kubernetes namespace
│   ├── 📄 configmap.yaml                 # Configuration management
│   ├── 📄 secret.yaml                    # Sensitive credentials
│   ├── 📄 postgres-statefulset.yaml      # PostgreSQL deployment
│   ├── 📄 backend-deployment.yaml        # Backend deployment & service
│   ├── 📄 frontend-deployment.yaml       # Frontend deployment & service
│   └── 📄 ingress.yaml                   # Ingress routing
│
├── 📂 argocd/
│   └── 📄 application.yaml               # Argo CD Application resource
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── 📄 ci-cd.yml                  # GitHub Actions CI/CD pipeline
│
├── 📂 docs/
│   ├── 📄 ARCHITECTURE.md                # System design & architecture
│   ├── 📄 CI-CD-SETUP.md                 # GitHub Actions setup guide
│   ├── 📄 KUBERNETES-DEPLOYMENT.md       # Detailed K8s commands
│   └── 📄 ARGOCD-SETUP.md                # Argo CD setup & troubleshooting
│
└── 📂 tests/
    └── 📄 [Reserved for load tests, E2E tests]

```

## 📋 File Descriptions

### Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project overview, architecture, and quick start |
| `QUICK-REFERENCE.md` | Quick command reference for all tools |
| `DEPLOYMENT-CHECKLIST.md` | Step-by-step checklist for deployment |
| `docker-compose.yml` | Docker Compose for local development |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore patterns |
| `init.sh` | Initialization script |

### Backend Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with all API endpoints |
| `models.py` | SQLAlchemy ORM models (Trainer, TrainingSlot, Booking) |
| `schemas.py` | Pydantic models for API request/response validation |
| `crud.py` | Database operations (Create, Read, Update, Delete) |
| `database.py` | SQLAlchemy session and engine setup |
| `config.py` | Configuration loading from environment |
| `test_main.py` | Pytest tests for health, trainers, bookings |
| `init_sample_data.py` | Script to populate database with sample data |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Multi-stage Docker image for backend |
| `pytest.ini` | Pytest configuration |

### Frontend Files

| File | Purpose |
|------|---------|
| `src/App.jsx` | Main component with React Router |
| `src/main.jsx` | React entry point |
| `src/api.js` | Axios client for API calls |
| `src/pages/HomePage.jsx` | Landing page |
| `src/pages/TrainersPage.jsx` | List all trainers |
| `src/pages/SlotsPage.jsx` | Show available training slots |
| `src/pages/BookingPage.jsx` | Create new booking |
| `src/pages/BookingsPage.jsx` | View and manage bookings |
| `index.html` | HTML template with global CSS |
| `vite.config.js` | Vite build configuration |
| `package.json` | npm dependencies |
| `Dockerfile` | Multi-stage build: Node builder + Nginx server |

### Kubernetes Files

| File | Purpose |
|------|---------|
| `namespace.yaml` | Create 'fitbook' namespace |
| `configmap.yaml` | Non-sensitive config (DB host, port, name) |
| `secret.yaml` | Sensitive data (DB username, password) |
| `postgres-statefulset.yaml` | PostgreSQL StatefulSet with PVC |
| `backend-deployment.yaml` | Backend deployment with 2 replicas + service |
| `frontend-deployment.yaml` | Frontend deployment + service |
| `ingress.yaml` | NGINX Ingress with routing rules |

### CI/CD & GitOps Files

| File | Purpose |
|------|---------|
| `.github/workflows/ci-cd.yml` | GitHub Actions CI/CD pipeline |
| `argocd/application.yaml` | Argo CD Application resource for GitOps |

### Documentation Files

| File | Purpose |
|------|---------|
| `docs/ARCHITECTURE.md` | Detailed system design and component interactions |
| `docs/CI-CD-SETUP.md` | GitHub Actions setup and pipeline explanation |
| `docs/KUBERNETES-DEPLOYMENT.md` | Comprehensive Kubernetes commands and deployment |
| `docs/ARGOCD-SETUP.md` | Argo CD installation and GitOps workflow |

## 🔑 Key Technologies by Component

### Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104.1 | Web framework |
| Uvicorn | 0.24.0 | ASGI server |
| SQLAlchemy | 2.0.23 | ORM |
| PostgreSQL | 16-alpine | Database |
| Pydantic | (built-in) | Validation |
| Pytest | 7.4.3 | Testing |
| Python | 3.11 | Runtime |

### Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18.2.0 | UI framework |
| Vite | 5.0.0 | Build tool |
| React Router | 6.20.0 | Routing |
| Axios | 1.6.2 | HTTP client |
| Node | 20-alpine | Runtime |
| Nginx | alpine | Web server |

### DevOps

| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Kubernetes | Production orchestration |
| Minikube | Local K8s cluster |
| Argo CD | GitOps deployment |
| GitHub Actions | CI/CD automation |

## 📊 API Endpoints

All endpoints support JSON request/response:

```
GET    /api/health                  # Health check
GET    /api/trainers                # List all trainers
GET    /api/slots                   # List all slots
GET    /api/slots/available         # List available slots
POST   /api/bookings                # Create booking
GET    /api/bookings                # List all bookings
DELETE /api/bookings/{id}           # Cancel booking
```

**Auto-generated documentation**: `http://localhost:8000/docs`

## 🗄️ Database Schema

### trainers
- `id` INTEGER PRIMARY KEY
- `name` STRING
- `specialization` STRING

### training_slots
- `id` INTEGER PRIMARY KEY
- `trainer_id` INTEGER FOREIGN KEY (trainers)
- `training_date` DATETIME
- `is_available` BOOLEAN

### bookings
- `id` INTEGER PRIMARY KEY
- `client_name` STRING
- `training_slot_id` INTEGER FOREIGN KEY (training_slots)
- `created_at` DATETIME

## 🔄 CI/CD Pipeline Stages

1. **Test Backend** - Run pytest on code changes
2. **Test Frontend** - Build React app to verify no errors
3. **Build & Push** (main branch only)
   - Build backend Docker image
   - Build frontend Docker image
   - Push to Docker Hub with tags: `latest` and commit SHA
4. **Update Manifests** - Update K8s yamls with new image tags
5. **Argo CD Sync** - Automatically detects and deploys changes

## 🐳 Docker Images

Two multi-stage builds for production optimization:

### Backend Image
1. Builder stage: Python slim + dependencies
2. Runtime: Minimal Python image with app only

### Frontend Image
1. Builder stage: Node + npm build
2. Runtime: Alpine Nginx serving static files

## ⚙️ Environment Setup

### Local Development (.env)
```
DB_USER=fitbook_user
DB_PASSWORD=fitbook_password
DB_NAME=fitbook_db
DEBUG=False
```

### Kubernetes (ConfigMap & Secret)
```
ConfigMap:
- DB_HOST=postgres-service
- DB_PORT=5432
- DB_NAME=fitbook_db

Secret:
- DB_USER=fitbook_user
- DB_PASSWORD=fitbook_password
```

## 📈 Scaling Configuration

| Component | Min Replicas | Max Replicas | Request | Limit |
|-----------|--------------|--------------|---------|-------|
| Backend | 2 | 5+ | 100m CPU, 256Mi | 500m CPU, 512Mi |
| Frontend | 1 | 3+ | 50m CPU, 128Mi | 200m CPU, 256Mi |
| PostgreSQL | 1 | N/A | 100m CPU, 256Mi | 500m CPU, 512Mi |

## 🔐 Security Configuration

### Secrets in Repository
- ✅ `.env` and `.env.*` in `.gitignore`
- ✅ `secret.yaml` marked as example
- ✅ No API keys/tokens in code

### Kubernetes Security
- ✅ Separate namespace for resources
- ✅ ConfigMap for non-sensitive data
- ✅ Secret for credentials
- ✅ Non-root containers (where possible)
- ✅ Resource limits defined
- ✅ Health checks configured

### Network Security
- ✅ Ingress for external access
- ✅ ClusterIP services (internal communication)
- ✅ CORS enabled on backend
- ✅ Database not exposed externally

## 📦 Dependencies Summary

### Backend (Python)
- FastAPI framework
- SQLAlchemy ORM
- PostgreSQL driver
- Uvicorn server
- Pytest for testing

### Frontend (JavaScript)
- React UI framework
- Vite build tool
- React Router for navigation
- Axios for HTTP requests
- Nginx for production serving

### Infrastructure
- Docker for containerization
- PostgreSQL for data persistence
- Kubernetes for orchestration
- Argo CD for GitOps

## 🚀 Deployment Paths

```
Development Path:
docker-compose up → localhost:3000 → Local testing

Git Push Path:
GitHub push → Actions pipeline → Docker Hub → K8s manifests → Argo CD → Kubernetes

Manual Kubernetes Path:
kubectl apply -f kubernetes/ → Cluster deployment → Access via Ingress
```

## 📝 Testing Coverage

### Backend Tests (pytest)
- ✅ Health endpoint
- ✅ Trainer CRUD
- ✅ Booking creation
- ✅ Booking cancellation
- ✅ Slot availability management

### Frontend Testing (Available)
- Ready for Jest/Vitest tests
- React Testing Library support
- Component tests structure in place

### Integration Testing
- Docker Compose for local E2E
- Kubernetes for cluster testing

## 🎯 Learning Outcomes

Students completing this project will understand:

1. **Application Development**
   - Modern Python web framework (FastAPI)
   - React for frontend UIs
   - Database design and ORM usage

2. **DevOps & Containerization**
   - Docker image optimization
   - Multi-stage builds
   - Container networking

3. **Orchestration**
   - Kubernetes concepts (Pods, Services, Deployments)
   - StatefulSets for databases
   - Ingress for routing

4. **CI/CD Automation**
   - GitHub Actions workflows
   - Automated testing and building
   - Image registry integration

5. **GitOps & IaC**
   - Infrastructure as Code
   - Argo CD continuous deployment
   - Git-driven infrastructure

---

**Project Created**: June 2024

**Last Updated**: June 2024

**Total Files**: 40+

**Total Lines of Code**: 2000+

**Documentation Pages**: 6

---

Happy learning! 🎓

