.PHONY: help build run stop restart logs clean test deploy

# Default target
help:
	@echo "🐳 Paystack Integration - Docker Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build Docker image"
	@echo "  make run       - Run container in background"
	@echo "  make dev       - Run with live reload (docker-compose)"
	@echo "  make stop      - Stop the container"
	@echo "  make restart   - Restart the container"
	@echo "  make logs      - View container logs"
	@echo "  make shell     - Open shell in container"
	@echo "  make test      - Test the application"
	@echo "  make clean     - Remove container and image"
	@echo "  make deploy    - Build and deploy"
	@echo ""

# Build Docker image
build:
	@echo "🔨 Building Docker image..."
	docker build -t paystack-app .
	@echo "✅ Build complete!"

# Run container
run:
	@echo "🚀 Starting container..."
	docker run -d \
		-p 8000:8000 \
		--env-file .env \
		--name paystack-app \
		paystack-app
	@echo "✅ Container started at http://localhost:8000"

# Development mode with docker-compose
dev:
	@echo "🛠️  Starting in development mode..."
	docker-compose up

# Stop container
stop:
	@echo "🛑 Stopping container..."
	docker stop paystack-app || true
	@echo "✅ Container stopped"

# Restart container
restart: stop run
	@echo "✅ Container restarted"

# View logs
logs:
	@echo "📋 Viewing logs (Ctrl+C to exit)..."
	docker logs -f paystack-app

# Open shell in container
shell:
	@echo "🐚 Opening shell..."
	docker exec -it paystack-app bash

# Test application
test:
	@echo "🧪 Testing application..."
	@curl -f http://localhost:8000/api/health && echo "✅ Health check passed" || echo "❌ Health check failed"

# Clean up
clean: stop
	@echo "🧹 Cleaning up..."
	docker rm paystack-app || true
	docker rmi paystack-app || true
	@echo "✅ Cleanup complete"

# Full deploy (build and run)
deploy: build run
	@echo "🎉 Deployment complete!"
	@echo "Access your app at: http://localhost:8000"

# Docker Compose commands
compose-up:
	docker-compose up -d
	@echo "✅ Services started with docker-compose"

compose-down:
	docker-compose down
	@echo "✅ Services stopped"

compose-logs:
	docker-compose logs -f

# Production build
prod-build:
	@echo "🏭 Building production image..."
	docker build -t paystack-app:prod .
	@echo "✅ Production build complete!"

# Push to registry (customize with your registry)
push:
	@echo "📤 Pushing to registry..."
	@read -p "Enter registry (e.g., docker.io/username): " REGISTRY; \
	docker tag paystack-app:latest $$REGISTRY/paystack-app:latest && \
	docker push $$REGISTRY/paystack-app:latest
	@echo "✅ Pushed to registry"
