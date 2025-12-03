# 🐳 Docker Quick Deployment Guide

Deploy your Paystack integration platform using Docker in just a few commands!

---

## 📋 Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- Paystack API keys

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Build the Docker image
docker build -t paystack-app .

# 2. Run the container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name paystack-integration \
  paystack-app

# 3. Open your browser
open http://localhost:8000
```

---

## 🐳 Using Docker Compose (Recommended)

### Start the Application

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## ⚙️ Configuration

### Environment Variables

Make sure your `.env` file contains:

```env
PAYSTACK_SECRET_KEY=sk_test_your_key
PAYSTACK_PUBLIC_KEY=pk_test_your_key
PAYSTACK_BASE_URL=https://api.paystack.co
APP_URL=http://localhost:8000
DEBUG=False
```

### Custom Port

To run on a different port:

```bash
# Using docker run
docker run -d -p 3000:8000 --env-file .env --name paystack-app paystack-app

# Using docker-compose (edit docker-compose.yml)
# Change ports: "3000:8000"
```

---

## 🔧 Docker Commands Cheat Sheet

### Build & Run

```bash
# Build image
docker build -t paystack-app .

# Run container
docker run -d -p 8000:8000 --env-file .env --name paystack-app paystack-app

# Run with custom environment variables
docker run -d -p 8000:8000 \
  -e PAYSTACK_SECRET_KEY=sk_test_xxx \
  -e PAYSTACK_PUBLIC_KEY=pk_test_xxx \
  -e APP_URL=http://localhost:8000 \
  --name paystack-app \
  paystack-app
```

### Container Management

```bash
# List running containers
docker ps

# View logs
docker logs paystack-app
docker logs -f paystack-app  # Follow logs

# Stop container
docker stop paystack-app

# Start container
docker start paystack-app

# Restart container
docker restart paystack-app

# Remove container
docker rm paystack-app

# Remove container (force)
docker rm -f paystack-app
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi paystack-app

# Build without cache
docker build --no-cache -t paystack-app .

# Tag image for registry
docker tag paystack-app your-registry/paystack-app:latest
```

### Debugging

```bash
# Execute commands in running container
docker exec -it paystack-app bash

# Check container health
docker inspect --format='{{.State.Health.Status}}' paystack-app

# View container resource usage
docker stats paystack-app
```

---

## 🌐 Deploy to Cloud with Docker

### 1. Docker Hub

```bash
# Login
docker login

# Tag image
docker tag paystack-app yourusername/paystack-app:latest

# Push to Docker Hub
docker push yourusername/paystack-app:latest

# Pull and run on any server
docker pull yourusername/paystack-app:latest
docker run -d -p 8000:8000 --env-file .env yourusername/paystack-app:latest
```

### 2. AWS ECS (Elastic Container Service)

```bash
# Install AWS CLI and configure
aws configure

# Create ECR repository
aws ecr create-repository --repository-name paystack-app

# Get login command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag paystack-app:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/paystack-app:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/paystack-app:latest

# Deploy to ECS using AWS Console or CLI
```

### 3. Google Cloud Run

```bash
# Install gcloud CLI
gcloud auth login

# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/paystack-app

# Deploy
gcloud run deploy paystack-app \
  --image gcr.io/YOUR_PROJECT_ID/paystack-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PAYSTACK_SECRET_KEY=sk_test_xxx,PAYSTACK_PUBLIC_KEY=pk_test_xxx
```

### 4. Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name paystack-rg --location eastus

# Create container registry
az acr create --resource-group paystack-rg --name paystackregistry --sku Basic

# Build and push
az acr build --registry paystackregistry --image paystack-app:latest .

# Deploy
az container create \
  --resource-group paystack-rg \
  --name paystack-app \
  --image paystackregistry.azurecr.io/paystack-app:latest \
  --dns-name-label paystack-app-unique \
  --ports 8000 \
  --environment-variables \
    PAYSTACK_SECRET_KEY=sk_test_xxx \
    PAYSTACK_PUBLIC_KEY=pk_test_xxx
```

### 5. DigitalOcean Container Registry

```bash
# Install doctl
doctl auth init

# Create registry
doctl registry create paystack

# Login
doctl registry login

# Tag and push
docker tag paystack-app registry.digitalocean.com/paystack/paystack-app:latest
docker push registry.digitalocean.com/paystack/paystack-app:latest

# Deploy using DigitalOcean App Platform or Kubernetes
```

### 6. Heroku Container Registry

```bash
# Login to Heroku
heroku login
heroku container:login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set PAYSTACK_SECRET_KEY=sk_test_xxx -a your-app-name
heroku config:set PAYSTACK_PUBLIC_KEY=pk_test_xxx -a your-app-name
heroku config:set APP_URL=https://your-app-name.herokuapp.com -a your-app-name

# Push and release
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name

# Open app
heroku open -a your-app-name
```

### 7. Railway (Easiest!)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to GitHub repo (recommended)
railway link

# Deploy
railway up

# Set environment variables in Railway dashboard
# Then redeploy
```

---

## 🔐 Production Best Practices

### 1. Use Secrets Management

```bash
# Docker Secrets (Swarm mode)
echo "sk_test_xxx" | docker secret create paystack_secret -
docker service create --secret paystack_secret paystack-app

# Use .env file but don't commit it
echo ".env" >> .gitignore
```

### 2. Enable HTTPS

```yaml
# docker-compose.yml with nginx and SSL
version: "3.8"
services:
  app:
    build: .
    expose:
      - 8000

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - app
```

### 3. Resource Limits

```bash
# Limit memory and CPU
docker run -d \
  --memory="512m" \
  --cpus="0.5" \
  -p 8000:8000 \
  --env-file .env \
  paystack-app
```

### 4. Health Checks

```bash
# The Dockerfile already includes health checks
# Monitor container health
docker inspect --format='{{json .State.Health}}' paystack-app | jq
```

### 5. Logging

```bash
# Configure logging driver
docker run -d \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -p 8000:8000 \
  --env-file .env \
  paystack-app
```

---

## 🧪 Testing Docker Build Locally

```bash
# Test build
docker build -t paystack-app:test .

# Run tests in container
docker run --rm paystack-app:test python -c "import main; print('OK')"

# Test with different environment
docker run -p 8000:8000 \
  -e DEBUG=True \
  -e APP_URL=http://localhost:8000 \
  --env-file .env \
  paystack-app
```

---

## 📊 Monitoring

### View Container Stats

```bash
# Real-time stats
docker stats paystack-app

# All containers
docker stats
```

### Check Logs

```bash
# Last 100 lines
docker logs --tail 100 paystack-app

# Follow logs
docker logs -f paystack-app

# Logs with timestamps
docker logs -t paystack-app
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker logs paystack-app

# Run interactively to see errors
docker run -it --rm --env-file .env paystack-app

# Check if port is already in use
lsof -i :8000
```

### Can't connect to application

```bash
# Check if container is running
docker ps

# Check port mapping
docker port paystack-app

# Test from inside container
docker exec paystack-app curl http://localhost:8000/api/health
```

### Environment variables not loading

```bash
# Print environment variables
docker exec paystack-app env

# Run with explicit variables
docker run -p 8000:8000 \
  -e PAYSTACK_SECRET_KEY=sk_test_xxx \
  -e PAYSTACK_PUBLIC_KEY=pk_test_xxx \
  paystack-app
```

### Image size too large

```bash
# Check image size
docker images paystack-app

# Use alpine base image (already using slim)
# Remove unnecessary files in .dockerignore

# Multi-stage build (optional)
# See Dockerfile.multistage for example
```

---

## 🔄 Update & Redeploy

```bash
# 1. Make code changes

# 2. Rebuild image
docker build -t paystack-app .

# 3. Stop old container
docker stop paystack-app
docker rm paystack-app

# 4. Run new container
docker run -d -p 8000:8000 --env-file .env --name paystack-app paystack-app

# OR with docker-compose
docker-compose down
docker-compose up --build -d
```

---

## 📝 Docker Compose Full Example

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: paystack-integration
    ports:
      - "8000:8000"
    environment:
      - PAYSTACK_SECRET_KEY=${PAYSTACK_SECRET_KEY}
      - PAYSTACK_PUBLIC_KEY=${PAYSTACK_PUBLIC_KEY}
      - PAYSTACK_BASE_URL=${PAYSTACK_BASE_URL}
      - APP_URL=${APP_URL}
      - DEBUG=${DEBUG}
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - paystack-net
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

networks:
  paystack-net:
    driver: bridge
```

---

## 🎯 Quick Deploy Checklist

- [ ] Docker installed
- [ ] `.env` file configured with Paystack keys
- [ ] Build image: `docker build -t paystack-app .`
- [ ] Run container: `docker run -d -p 8000:8000 --env-file .env --name paystack-app paystack-app`
- [ ] Test: `curl http://localhost:8000/api/health`
- [ ] Access app: http://localhost:8000
- [ ] Configure Paystack webhook URL
- [ ] Test payment with test cards

---

## 🚀 One-Line Deploy

```bash
docker build -t paystack-app . && docker run -d -p 8000:8000 --env-file .env --name paystack-app paystack-app && echo "App running at http://localhost:8000"
```

---

## 📞 Need Help?

- Docker docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose/
- Troubleshooting: Check container logs with `docker logs paystack-app`

---

**Your Paystack integration is now Dockerized and ready for deployment anywhere!** 🐳🚀
