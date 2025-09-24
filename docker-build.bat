@echo off
REM Docker Build Script for Titanic Survival Prediction System
REM This script builds all Docker images for the application

echo 🚢 Building Titanic Survival Prediction System Docker Images
echo ==============================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Build ML Model image
echo [INFO] Building ML Model image...
docker build -t titanic-ml-model ./ml-model
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build ML Model image
    exit /b 1
)
echo [SUCCESS] ML Model image built successfully

REM Build FastAPI Backend image
echo [INFO] Building FastAPI Backend image...
docker build -t titanic-fastapi-backend ./fastapi-backend
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build FastAPI Backend image
    exit /b 1
)
echo [SUCCESS] FastAPI Backend image built successfully

REM Build Java Frontend image
echo [INFO] Building Java Frontend image...
docker build -t titanic-java-frontend ./java-frontend
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build Java Frontend image
    exit /b 1
)
echo [SUCCESS] Java Frontend image built successfully

echo [SUCCESS] All Docker images built successfully!
echo.
echo 📋 Available images:
docker images | findstr titanic

echo.
echo 🚀 To run the application, use:
echo    docker-run.bat
echo.
echo 🔧 To run with docker-compose:
echo    docker-compose up -d
