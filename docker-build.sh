#!/bin/bash

# Docker Build Script for Titanic Survival Prediction System
# This script builds all Docker images for the application

set -e

echo "🚢 Building Titanic Survival Prediction System Docker Images"
echo "=============================================================="

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

# Build ML Model image
print_status "Building ML Model image..."
if docker build -t titanic-ml-model ./ml-model; then
    print_success "ML Model image built successfully"
else
    print_error "Failed to build ML Model image"
    exit 1
fi

# Build FastAPI Backend image
print_status "Building FastAPI Backend image..."
if docker build -t titanic-fastapi-backend ./fastapi-backend; then
    print_success "FastAPI Backend image built successfully"
else
    print_error "Failed to build FastAPI Backend image"
    exit 1
fi

# Build Java Frontend image
print_status "Building Java Frontend image..."
if docker build -t titanic-java-frontend ./java-frontend; then
    print_success "Java Frontend image built successfully"
else
    print_error "Failed to build Java Frontend image"
    exit 1
fi

print_success "All Docker images built successfully!"
echo ""
echo "📋 Available images:"
docker images | grep titanic

echo ""
echo "🚀 To run the application, use:"
echo "   ./docker-run.sh"
echo ""
echo "🔧 To run with docker-compose:"
echo "   docker-compose up -d"
