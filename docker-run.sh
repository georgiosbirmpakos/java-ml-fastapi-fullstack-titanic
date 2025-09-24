#!/bin/bash

# Docker Run Script for Titanic Survival Prediction System
# This script runs the complete application using Docker Compose

set -e

echo "🚢 Starting Titanic Survival Prediction System"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Parse command line arguments
MODE="dev"
TRAIN_MODEL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            MODE="prod"
            shift
            ;;
        --train)
            TRAIN_MODEL=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --prod     Run in production mode with nginx proxy"
            echo "  --train    Train the ML model before starting services"
            echo "  --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run in development mode"
            echo "  $0 --prod             # Run in production mode"
            echo "  $0 --train            # Train model and run in dev mode"
            echo "  $0 --prod --train     # Train model and run in production mode"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Set compose file based on mode
if [ "$MODE" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    print_status "Running in production mode"
else
    COMPOSE_FILE="docker-compose.yml"
    print_status "Running in development mode"
fi

# Train model if requested
if [ "$TRAIN_MODEL" = true ]; then
    print_status "Training ML model..."
    if [ "$MODE" = "prod" ]; then
        docker-compose -f $COMPOSE_FILE --profile training up ml-trainer
    else
        # For dev mode, we'll train the model as part of the ml-model service
        print_warning "Model training will happen automatically in development mode"
    fi
fi

# Start services
print_status "Starting services with $COMPOSE_FILE..."

if docker-compose -f $COMPOSE_FILE up -d; then
    print_success "Services started successfully!"
else
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be ready
print_status "Waiting for services to be ready..."

# Wait for FastAPI backend
print_status "Waiting for FastAPI backend..."
timeout=60
while [ $timeout -gt 0 ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "FastAPI backend is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_warning "FastAPI backend did not start within 60 seconds"
fi

# Wait for Java frontend
print_status "Waiting for Java frontend..."
timeout=120
while [ $timeout -gt 0 ]; do
    if curl -f http://localhost:8080/ > /dev/null 2>&1; then
        print_success "Java frontend is ready!"
        break
    fi
    sleep 3
    timeout=$((timeout - 3))
done

if [ $timeout -le 0 ]; then
    print_warning "Java frontend did not start within 120 seconds"
fi

echo ""
echo "🎉 Application is running!"
echo ""
echo "📱 Access the application:"
echo "   Frontend (Java): http://localhost:8080"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo ""

if [ "$MODE" = "prod" ]; then
    echo "🌐 With nginx proxy:"
    echo "   Frontend: http://localhost"
    echo "   API:      http://localhost/api"
fi

echo ""
echo "📊 Check service status:"
echo "   docker-compose -f $COMPOSE_FILE ps"
echo ""
echo "📝 View logs:"
echo "   docker-compose -f $COMPOSE_FILE logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose -f $COMPOSE_FILE down"
