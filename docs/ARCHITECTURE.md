# FitBook Architecture & Design

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                            │
│  (Code + Kubernetes Manifests)                                   │
└────────────────┬──────────────────────────────┬─────────────────┘
                 │                              │
         ┌───────▼──────────┐          ┌────────▼────────┐
         │ GitHub Actions   │          │    Argo CD      │
         │                  │          │                 │
         │ 1. Tests         │          │ 1. Monitors repo│
         │ 2. Builds        │          │ 2. Syncs Config │
         │ 3. Pushes Images │          │ 3. Deploys Apps │
         └───────┬──────────┘          └────────┬────────┘
                 │                              │
         ┌───────▼──────────────┐              │
         │   Docker Hub         │◄─────────────┘
         │   (Image Registry)   │
         └──────────────────────┘
                 │
         ┌───────▼────────────────────┐
         │   Kubernetes Cluster       │
         │   (Minikube for Testing)   │
         │                            │
         │  ┌──────────────────────┐  │
         │  │ Namespace: fitbook   │  │
         │  │                      │  │
         │  │ ┌──────────────────┐ │  │
         │  │ │ Frontend Pod     │ │  │
         │  │ │ (Nginx)          │ │  │
         │  │ └──────────────────┘ │  │
         │  │          │           │  │
         │  │ ┌────────▼────────┐  │  │
         │  │ │ Backend Pod(s)  │  │  │
         │  │ │ (FastAPI)       │  │  │
         │  │ └────────┬────────┘  │  │
         │  │          │           │  │
         │  │ ┌────────▼────────┐  │  │
         │  │ │ PostgreSQL Pod  │  │  │
         │  │ │ (StatefulSet)   │  │  │
         │  │ └─────────────────┘  │  │
         │  └──────────────────────┘  │
         └────────────────────────────┘
```

## Component Details

### Frontend (React + Vite)

**Purpose**: User interface for the FitBook application

**Components**:
- `HomePage`: Landing page with introduction
- `TrainersPage`: Display list of all trainers
- `SlotsPage`: Show available training sessions
- `BookingPage`: Form to create new bookings
- `BookingsPage`: Manage existing bookings

**Communication**:
- Axios HTTP client for API calls
- Proxy configuration in Vite for development
- Environment-based API URL configuration

**Deployment**:
- Multi-stage Docker build (build stage → Nginx serve stage)
- Nginx handles SPA routing and static asset caching
- API proxy to backend through Nginx

### Backend (FastAPI)

**Purpose**: RESTful API and business logic

**Modules**:
- `main.py`: FastAPI application and route handlers
- `models.py`: SQLAlchemy database models
- `schemas.py`: Pydantic validation models
- `crud.py`: Database operations
- `database.py`: SQLAlchemy session management
- `config.py`: Application configuration

**Key Features**:
- CORS enabled for frontend communication
- Health check endpoint for monitoring
- Dependency injection for database sessions
- Automatic API documentation at `/docs`

**Database Relationships**:
```
Trainer (1) ─── (Many) TrainingSlot
                           │
                       (1) │
                           ▼
                      Booking (Many)
```

### Database (PostgreSQL)

**Purpose**: Persistent data storage

**Tables**:
1. `trainers`: Trainer information
2. `training_slots`: Available training sessions
3. `bookings`: User bookings

**Key Operations**:
- Booking creation automatically marks slot as unavailable
- Booking cancellation marks slot as available again
- Relationships enforced via foreign keys

**Data Persistence**:
- StatefulSet with PersistentVolumeClaim
- Data survives pod restarts/migrations
- Single replica for simplicity (can scale in production)

## Deployment Environments

### Development (Local - Docker Compose)

```yaml
Services:
  - PostgreSQL: localhost:5432
  - Backend: localhost:8000
  - Frontend: localhost:3000

Network: fitbook-network (bridge)
Volumes: postgres_data (named volume)
```

**Advantages**:
- Quick start for development
- Full application on single machine
- Easy debugging with live logs

### Production (Kubernetes)

```yaml
Namespace: fitbook

Components:
  - Ingress Controller (NGINX)
  - Frontend Deployment (1-N replicas)
  - Backend Deployment (2+ replicas)
  - PostgreSQL StatefulSet (1 replica)
  - Services (ClusterIP)
  - ConfigMap & Secret
  - PersistentVolumeClaim
```

**Advantages**:
- High availability with multiple replicas
- Automatic scaling capabilities
- Better resource management
- Health checks and auto-recovery

## CI/CD Pipeline Flow

```
1. Developer Commits & Pushes to GitHub
         │
         ▼
2. GitHub Actions Triggered
         │
    ┌────┴─────┬──────────┐
    │           │          │
    ▼           ▼          ▼
Test Backend  Test Frontend Parallel Tests
    │           │          │
    └────┬──────┴──────────┘
         │
         ▼
3. All Tests Pass?
    ├─ No → Failed, notify developer
    │
    └─ Yes ──┐
             ▼
4. Main branch & Push Event?
    ├─ No → Skip build
    │
    └─ Yes ──┐
             ▼
5. Build Docker Images
    ├─ Backend image
    └─ Frontend image
             │
             ▼
6. Login to Docker Hub
             │
             ▼
7. Push Images with Tags
    ├─ latest
    └─ Commit SHA
             │
             ▼
8. Update Kubernetes Manifests
    └─ Replace image tags with commit SHA
             │
             ▼
9. Commit Changes [skip ci]
             │
             ▼
10. Push to GitHub
             │
             ▼
11. Argo CD Detects Changes
             │
             ▼
12. Sync Kubernetes Manifests
             │
             ▼
13. Deploy New Images
             │
             ▼
14. Application Updated ✓
```

## Key Architectural Decisions

### 1. **Separate Docker Images**
- Each service has its own image
- Enables independent scaling
- Clear separation of concerns
- Faster deployments for individual services

### 2. **PostgreSQL in Kubernetes**
- StatefulSet for persistent identity
- PersistentVolumeClaim for data persistence
- ConfigMap for non-sensitive config
- Secret for credentials

### 3. **Nginx Frontend Proxy**
- Handles SPA routing (`try_files` directive)
- Proxies API calls to backend
- Static asset caching
- Better performance than serving React directly

### 4. **Ingress Controller**
- Single entry point (fitbook.local)
- Routing rules for frontend and backend
- TLS termination point (in production)

### 5. **Argo CD for GitOps**
- Infrastructure as Code
- Git as single source of truth
- Automatic synchronization
- Easy rollbacks via Git history

## Communication Patterns

### 1. Frontend → Backend (HTTP/REST)

```
Browser Request
     │
     ▼
Frontend (http://fitbook.local/)
     │ (Nginx proxy)
     ▼
Backend API (http://backend-service:8000/api)
     │
     ▼
Response JSON
     │
     ▼
Browser Updates UI
```

### 2. Backend → Database (SQL)

```
FastAPI Request
     │
     ▼
SQLAlchemy ORM
     │
     ▼
PostgreSQL Connection
     │
     ▼
SQL Query
     │
     ▼
Database Response
     │
     ▼
Python Objects
     │
     ▼
JSON Response to Frontend
```

### 3. CI/CD Pipeline → Docker Hub

```
GitHub Actions Runner
     │
     ├─ Build Backend Image
     ├─ Build Frontend Image
     │
     ▼
Docker Authentication
     │
     ├─ Push: dockerhub/fitbook-backend:v1.0.0
     └─ Push: dockerhub/fitbook-frontend:v1.0.0
```

### 4. Argo CD → Kubernetes

```
Argo CD Controller
     │
     ├─ Poll GitHub Repository
     │
     ├─ Detect Changes in /kubernetes
     │
     ├─ Compare with Kubernetes State
     │
     ├─ Apply Differences
     │
     ▼
Kubernetes API Server
     │
     ├─ Create/Update Resources
     │
     ├─ Trigger Pod Scheduling
     │
     ▼
Application Running ✓
```

## Security Considerations

### Current Implementation (Development)

- ✅ Secrets in Kubernetes Secret object
- ✅ CORS enabled for all origins (development mode)
- ✅ Environment-based configuration
- ❓ Basic health checks only

### Production Recommendations

- 🔐 **Sealed Secrets** or **SopsEnc** for encrypted secrets in Git
- 🔐 **Network Policies** to restrict pod-to-pod communication
- 🔐 **RBAC** (Role-Based Access Control) for service accounts
- 🔐 **TLS/SSL** termination at Ingress
- 🔐 **API Rate Limiting** for backend endpoints
- 🔐 **Authentication & Authorization** (JWT, OAuth2)
- 🔐 **Pod Security Policies** to restrict containers
- 📊 **Audit Logging** for compliance

## Scaling Strategy

### Horizontal Scaling

```yaml
Frontend:
  - Replicas: 1 → N (Nginx handles load balancing)
  - Stateless: No session storage needed
  - Quick autoscaling possible

Backend:
  - Replicas: 2 → N (Share database)
  - Stateless API: No server affinity needed
  - Database becomes bottleneck at scale

Database:
  - Single replica (can upgrade to multi-node cluster)
  - Implement read replicas for read-heavy workloads
  - Consider managed database services (RDS, Cloud SQL)
```

### Vertical Scaling

- Increase resource requests/limits
- Use more powerful VM instances
- Upgrade PostgreSQL server specs

## Monitoring & Observability

### Metrics to Monitor

```
Infrastructure:
- CPU usage per pod
- Memory consumption per service
- Network I/O
- Disk usage (especially PostgreSQL)
- Pod restart counts

Application:
- API response times
- Request error rates
- Database query performance
- Cache hit ratios

Business:
- Active trainers
- Available slots
- Bookings per day
- User conversion rates
```

### Tools Recommendation

- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Logging and analysis
- **Jaeger**: Distributed tracing

---

**Last Updated**: June 2024

