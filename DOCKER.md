# 🐳 Docker Setup for Titanic Survival Prediction System

This document provides comprehensive instructions for running the Titanic Survival Prediction System using Docker containers.

## 📋 Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **Git** (for cloning the repository)
- **8GB+ RAM** (recommended for smooth operation)

## 🚀 Quick Start

### Option 1: Using Helper Scripts (Recommended)

#### Windows:
```cmd
# Build all Docker images
docker-build.bat

# Run the application
docker-run.bat
```

#### Linux/Mac:
```bash
# Make scripts executable
chmod +x docker-build.sh docker-run.sh

# Build all Docker images
./docker-build.sh

# Run the application
./docker-run.sh
```

### Option 2: Using Docker Compose Directly

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🏗️ Architecture Overview

The Docker setup consists of four main services:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Java Frontend │    │  FastAPI Backend│    │   ML Model      │
│   (Tomcat 10)   │◄──►│   (Python 3.11) │◄──►│   (Scikit-learn)│
│   Port: 8080     │    │   Port: 8000     │    │   Training Only │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        ▲                        ▲
         │                        │                        │
         ▼                        │                        │
┌─────────────────┐              │                        │
│  AI Chatbot     │──────────────┘                        │
│  (Python 3.11) │                                       │
│  Port: 8010     │                                       │
└─────────────────┘                                       │
         │                                                │
         ▼                                                │
┌─────────────────┐                                       │
│     Nginx       │───────────────────────────────────────┘
│  (Port 80/443)  │
└─────────────────┘
```

## 📁 Docker Files Structure

```
├── docker-compose.yml          # Development compose file
├── docker-compose.prod.yml     # Production compose file
├── docker-build.sh/.bat        # Build script
├── docker-run.sh/.bat          # Run script
├── nginx.conf                  # Nginx reverse proxy config
├── .dockerignore               # Global dockerignore
├── ml-model/
│   ├── Dockerfile              # ML model container
│   ├── requirements.txt        # Python dependencies
│   └── .dockerignore           # ML-specific ignores
├── fastapi-backend/
│   ├── Dockerfile              # FastAPI container
│   ├── requirements.txt        # Python dependencies
│   └── .dockerignore           # API-specific ignores
├── chatbot-service/
│   ├── Dockerfile              # AI Chatbot container
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # OpenAI API configuration
│   └── .dockerignore           # Chatbot-specific ignores
└── java-frontend/
    ├── Dockerfile              # Java/Tomcat container
    └── .dockerignore           # Java-specific ignores
```

## 🔧 Service Details

### 1. ML Model Service (`ml-model`)

**Purpose**: Trains the machine learning model and provides prediction utilities

**Image**: `titanic-ml-model`
**Base**: `python:3.11-slim`
**Port**: Internal only
**Volumes**: 
- `./ml-model/models:/app/models`
- `./ml-model/data:/app/data`

**Features**:
- Downloads Titanic dataset automatically
- Trains Random Forest classifier
- Saves trained models and encoders
- Provides prediction utilities

### 2. FastAPI Backend Service (`fastapi-backend`)

**Purpose**: RESTful API server for ML predictions

**Image**: `titanic-fastapi-backend`
**Base**: `python:3.11-slim`
**Port**: `8000`
**Volumes**: 
- `./ml-model/models:/app/models:ro` (read-only)

**Features**:
- Loads trained ML models
- Provides REST API endpoints
- Health monitoring
- CORS support
- Interactive API documentation

**Endpoints**:
- `GET /health` - Health check
- `POST /predict` - Single prediction
- `GET /docs` - API documentation

### 3. AI Chatbot Service (`chatbot-service`)

**Purpose**: AI-powered chatbot for natural language passenger predictions

**Image**: `titanic-chatbot-service`
**Base**: `python:3.11-slim`
**Port**: `8010`
**Environment**: 
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL=gpt-4o-mini` (default)

**Features**:
- OpenAI GPT-4o mini integration
- LangChain-based natural language processing
- Manual fallback extraction rules
- FastAPI integration with ML backend
- Health monitoring and status endpoints

**Endpoints**:
- `GET /test` - Health check
- `GET /health` - Service health status
- `POST /predict-nl` - Natural language prediction
- `GET /docs` - API documentation

### 4. Java Frontend Service (`java-frontend`)

**Purpose**: Web application frontend using JSF and PrimeFaces

**Image**: `titanic-java-frontend`
**Base**: `tomcat:10.1-jdk17-openjdk-slim`
**Port**: `8080`
**Environment**: 
- `JAVA_OPTS=-Xmx512m -Xms256m`

**Features**:
- Dual interface: Traditional ML and AI chatbot approaches
- Modern web UI with PrimeFaces
- Form validation and natural language processing
- Real-time API communication with both services
- Responsive design
- Sample passenger data and preset examples
- Interactive AI chatbot with 5 preset scenarios

## 🚀 Running Modes

### Development Mode

```bash
# Using helper script
./docker-run.sh

# Using docker-compose directly
docker-compose up -d
```

**Features**:
- Hot reloading for development
- Detailed logging
- Direct port access
- Simplified networking

### Production Mode

```bash
# Using helper script
./docker-run.sh --prod

# Using docker-compose directly
docker-compose -f docker-compose.prod.yml up -d
```

**Features**:
- Nginx reverse proxy
- Optimized resource usage
- Production-ready configuration
- Health checks
- Restart policies

### Training Mode

```bash
# Train model and run in development
./docker-run.sh --train

# Train model and run in production
./docker-run.sh --prod --train
```

## 🔍 Service Management

### Check Service Status

```bash
# View running containers
docker-compose ps

# Check service health
docker-compose exec fastapi-backend curl http://localhost:8000/health
docker-compose exec java-frontend curl http://localhost:8080/
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi-backend
docker-compose logs -f java-frontend
docker-compose logs -f ml-model
```

### Access Services

```bash
# Access FastAPI backend shell
docker-compose exec fastapi-backend bash

# Access Java frontend shell
docker-compose exec java-frontend bash

# Access ML model shell
docker-compose exec ml-model bash
```

## 🌐 Network Configuration

### Development Network
- **Network**: `titanic-network` (bridge)
- **Frontend**: `http://localhost:8080`
- **Backend**: `http://localhost:8000`
- **Chatbot**: `http://localhost:8010`
- **API Docs**: `http://localhost:8000/docs`
- **Chatbot API Docs**: `http://localhost:8010/docs`

### Production Network
- **Network**: `titanic-network` (bridge)
- **Frontend**: `http://localhost` (via nginx)
- **Backend**: `http://localhost/api` (via nginx)
- **Chatbot**: `http://localhost/chatbot` (via nginx)
- **Direct Backend**: `http://localhost:8000`
- **Direct Chatbot**: `http://localhost:8010`

## 📊 Monitoring and Health Checks

### Health Check Endpoints

```bash
# FastAPI backend health
curl http://localhost:8000/health

# AI Chatbot service health
curl http://localhost:8010/test

# Java frontend health
curl http://localhost:8080/

# Nginx health (production mode)
curl http://localhost/health
```

### Container Health Status

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Detailed health info
docker inspect titanic-fastapi-backend | grep -A 10 Health
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Port 8080 is already allocated`

**Solution**:
```bash
# Stop conflicting services
docker-compose down

# Or change ports in docker-compose.yml
ports:
  - "8081:8080"  # Change external port
```

#### 2. ML Model Not Loading

**Error**: `ML model not available`

**Solution**:
```bash
# Check if models exist
ls -la ml-model/models/

# Rebuild ML model
docker-compose up --build ml-model

# Check model loading logs
docker-compose logs ml-model
```

#### 3. Java Frontend Not Starting

**Error**: `Java frontend did not start within 120 seconds`

**Solution**:
```bash
# Check Java frontend logs
docker-compose logs java-frontend

# Increase memory allocation
# Edit docker-compose.yml:
environment:
  - JAVA_OPTS=-Xmx1024m -Xms512m
```

#### 4. FastAPI Backend Connection Issues

**Error**: `Connection refused`

**Solution**:
```bash
# Check if backend is running
docker-compose ps fastapi-backend

# Check backend logs
docker-compose logs fastapi-backend

# Restart backend
docker-compose restart fastapi-backend
```

### Debug Mode

```bash
# Run with debug logging
docker-compose up --build

# Run specific service in foreground
docker-compose up ml-model

# Run with verbose output
docker-compose --verbose up -d
```

## 🔄 Updates and Maintenance

### Rebuilding Images

```bash
# Rebuild all images
docker-compose build --no-cache

# Rebuild specific service
docker-compose build --no-cache fastapi-backend

# Using helper script
./docker-build.sh
```

### Updating Dependencies

```bash
# Update Python dependencies
# Edit requirements.txt files, then:
docker-compose build --no-cache

# Update Java dependencies
# Edit pom.xml, then:
docker-compose build --no-cache java-frontend
```

### Data Persistence

```bash
# View volumes
docker volume ls

# Backup model data
docker run --rm -v titanic_ml-models:/data -v $(pwd):/backup alpine tar czf /backup/models-backup.tar.gz -C /data .

# Restore model data
docker run --rm -v titanic_ml-models:/data -v $(pwd):/backup alpine tar xzf /backup/models-backup.tar.gz -C /data
```

## 🚀 Performance Optimization

### Resource Limits

```yaml
# Add to docker-compose.yml
services:
  fastapi-backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Scaling Services

```bash
# Scale FastAPI backend (requires load balancer)
docker-compose up -d --scale fastapi-backend=3

# Scale Java frontend (requires session affinity)
docker-compose up -d --scale java-frontend=2
```

## 🔒 Security Considerations

### Production Security

1. **Use specific image tags** instead of `latest`
2. **Run as non-root user** in containers
3. **Use secrets management** for sensitive data
4. **Enable HTTPS** with SSL certificates
5. **Implement network policies** for service isolation

### Example Security Configuration

```yaml
# docker-compose.prod.yml
services:
  fastapi-backend:
    user: "1000:1000"  # Non-root user
    read_only: true     # Read-only filesystem
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tomcat Documentation](https://tomcat.apache.org/tomcat-10.1-doc/)

## 🤝 Contributing

When contributing to the Docker setup:

1. Test changes in both development and production modes
2. Update documentation for any new features
3. Ensure backward compatibility
4. Add appropriate health checks
5. Update helper scripts if needed

---

**Happy Dockerizing! 🐳**
