@echo off
REM Docker Run Script for Titanic Survival Prediction System
REM This script runs the complete application using Docker Compose

echo 🚢 Starting Titanic Survival Prediction System
echo ==============================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] docker-compose is not installed. Please install docker-compose and try again.
    exit /b 1
)

REM Parse command line arguments
set MODE=dev
set TRAIN_MODEL=false

:parse_args
if "%1"=="--prod" (
    set MODE=prod
    shift
    goto parse_args
)
if "%1"=="--train" (
    set TRAIN_MODEL=true
    shift
    goto parse_args
)
if "%1"=="--help" (
    echo Usage: %0 [OPTIONS]
    echo.
    echo Options:
    echo   --prod     Run in production mode with nginx proxy
    echo   --train    Train the ML model before starting services
    echo   --help     Show this help message
    echo.
    echo Examples:
    echo   %0                    # Run in development mode
    echo   %0 --prod             # Run in production mode
    echo   %0 --train            # Train model and run in dev mode
    echo   %0 --prod --train     # Train model and run in production mode
    exit /b 0
)
if not "%1"=="" (
    echo [ERROR] Unknown option: %1
    echo Use --help for usage information
    exit /b 1
)

REM Set compose file based on mode
if "%MODE%"=="prod" (
    set COMPOSE_FILE=docker-compose.prod.yml
    echo [INFO] Running in production mode
) else (
    set COMPOSE_FILE=docker-compose.yml
    echo [INFO] Running in development mode
)

REM Train model if requested
if "%TRAIN_MODEL%"=="true" (
    echo [INFO] Training ML model...
    if "%MODE%"=="prod" (
        docker-compose -f %COMPOSE_FILE% --profile training up ml-trainer
    ) else (
        echo [WARNING] Model training will happen automatically in development mode
    )
)

REM Start services
echo [INFO] Starting services with %COMPOSE_FILE%...

docker-compose -f %COMPOSE_FILE% up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    exit /b 1
)

echo [SUCCESS] Services started successfully!

REM Wait for services to be ready
echo [INFO] Waiting for services to be ready...

REM Wait for FastAPI backend
echo [INFO] Waiting for FastAPI backend...
set timeout=60
:wait_fastapi
if %timeout% leq 0 (
    echo [WARNING] FastAPI backend did not start within 60 seconds
    goto wait_frontend
)
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] FastAPI backend is ready!
    goto wait_frontend
)
timeout /t 2 >nul
set /a timeout-=2
goto wait_fastapi

:wait_frontend
REM Wait for Java frontend
echo [INFO] Waiting for Java frontend...
set timeout=120
:wait_java
if %timeout% leq 0 (
    echo [WARNING] Java frontend did not start within 120 seconds
    goto show_info
)
curl -f http://localhost:8080/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Java frontend is ready!
    goto show_info
)
timeout /t 3 >nul
set /a timeout-=3
goto wait_java

:show_info
echo.
echo 🎉 Application is running!
echo.
echo 📱 Access the application:
echo    Frontend (Java): http://localhost:8080
echo    Backend API:     http://localhost:8000
echo    API Docs:        http://localhost:8000/docs
echo.

if "%MODE%"=="prod" (
    echo 🌐 With nginx proxy:
    echo    Frontend: http://localhost
    echo    API:      http://localhost/api
)

echo.
echo 📊 Check service status:
echo    docker-compose -f %COMPOSE_FILE% ps
echo.
echo 📝 View logs:
echo    docker-compose -f %COMPOSE_FILE% logs -f
echo.
echo 🛑 Stop services:
echo    docker-compose -f %COMPOSE_FILE% down
