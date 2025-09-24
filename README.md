# Titanic Survival Prediction System

A full-stack machine learning application that predicts passenger survival on the Titanic using historical data. The system consists of a Python ML model, FastAPI backend, and Java frontend with modern web technologies.

## ⚡ Quick Start (30 seconds)

```bash
git clone <repository-url>
cd java-ml-fastapi-fullstack-titanic
docker-compose up -d
```

**Access**: http://localhost:8080 (Frontend) | http://localhost:8000 (API)

> **That's it!** The application automatically downloads data, trains the ML model, and starts all services.

## 🚢 Project Overview

This project demonstrates a complete machine learning pipeline from data preprocessing to web deployment:

- **Machine Learning Model**: Trained Random Forest classifier for survival prediction
- **FastAPI Backend**: RESTful API serving ML predictions with health monitoring
- **Java Frontend**: Modern web application using JSF, PrimeFaces, and Jakarta EE
- **Full Integration**: End-to-end prediction workflow with real-time API communication

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    ML Model    ┌─────────────────┐
│   Java Frontend │ ──────────────► │  FastAPI Backend│ ─────────────► │   ML Pipeline   │
│   (JSF/PrimeFaces)│                │   (Python)      │                │   (Scikit-learn)│
└─────────────────┘                 └─────────────────┘                └─────────────────┘
```

## 📁 Project Structure

```
test_project/
├── ml-model/                 # Machine Learning Pipeline
│   ├── data/                 # Training datasets
│   ├── models/               # Trained models & encoders
│   ├── notebooks/            # Jupyter analysis notebooks
│   ├── train.py             # Model training script
│   └── predict.py           # Prediction script
├── fastapi-backend/          # Python API Server
│   ├── app.py               # FastAPI application
│   ├── models/              # Pydantic data models
│   └── notebooks/           # Educational content
├── java-frontend/            # Java Web Application
│   ├── src/main/java/       # Java source code
│   ├── src/main/webapp/     # Web resources (JSF pages)
│   ├── pom.xml              # Maven configuration
│   └── target/              # Build output
└── README.md                # This file
```

## 🚀 Quick Start - Plug & Play Setup

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **8GB+ RAM** (recommended)
- **Git**

### One-Command Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd java-ml-fastapi-fullstack-titanic
   ```

2. **Run the Complete Application**
   
   **Windows:**
   ```cmd
   .\docker-build.bat
   .\docker-run.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x docker-build.sh docker-run.sh
   ./docker-build.sh
   ./docker-run.sh
   ```
   
   **Or using Docker Compose directly:**
   ```bash
   docker-compose up -d
   ```

3. **Access the Application**
   - **Frontend**: http://localhost:8080
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### What Happens Automatically

✅ **ML Model Training**: Downloads Titanic dataset and trains Random Forest model  
✅ **FastAPI Backend**: Starts REST API server with trained model  
✅ **Java Frontend**: Builds and deploys JSF/PrimeFaces web application  
✅ **Network Configuration**: Sets up container communication  
✅ **Health Monitoring**: Built-in health checks for all services  

### Production Deployment

For production with nginx reverse proxy:
```bash
# Windows
.\docker-run.bat --prod

# Linux/Mac  
./docker-run.bat --prod

# Or directly
docker-compose -f docker-compose.prod.yml up -d
```

**Production Access Points:**
- **Frontend**: http://localhost
- **API**: http://localhost/api

## 🔧 Troubleshooting

### Common Issues

**❌ "Failed to get prediction from API"**
- **Solution**: Ensure all containers are running: `docker-compose ps`
- **Check**: FastAPI backend logs: `docker-compose logs fastapi-backend`

**❌ "Port already in use"**
- **Solution**: Stop conflicting services or change ports in `docker-compose.yml`
- **Check**: `netstat -an | findstr :8000` (Windows) or `lsof -i :8000` (Linux/Mac)

**❌ "ML model not loading"**
- **Solution**: Rebuild ML model: `docker-compose up --build ml-model`
- **Check**: Model files exist in `ml-model/models/` directory

**❌ "Java frontend not starting"**
- **Solution**: Check Java logs: `docker-compose logs java-frontend`
- **Increase memory**: Edit `docker-compose.yml` JAVA_OPTS to `-Xmx1024m -Xms512m`

### Service Management

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart fastapi-backend

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

### Manual Setup (Alternative)

If you prefer to run without Docker:

1. **Train ML Model**: `cd ml-model && pip install -r requirements.txt && python train.py`
2. **Start FastAPI**: `cd fastapi-backend && pip install -r requirements.txt && python app.py`
3. **Update Java Config**: Change `API_BASE_URL` to `http://localhost:8000` in `TitanicApiService.java`
4. **Build Java Frontend**: `cd java-frontend && mvn clean package`
5. **Deploy to Tomcat**: Copy `target/titanic-1.0.0.war` to Tomcat webapps directory

For detailed Docker documentation, see [DOCKER.md](DOCKER.md).

## 🎬 Demo

Once running, you can:

1. **Open the Frontend**: Navigate to http://localhost:8080
2. **Test Sample Data**: Click "Load Sample Passengers" to see historical Titanic passengers
3. **Make Predictions**: Fill out the form with passenger details and get survival predictions
4. **Check API Health**: Monitor the backend API status in real-time
5. **Explore API**: Visit http://localhost:8000/docs for interactive API documentation

### Sample Prediction

Try predicting survival for:
- **John Astor** (1st class male, age 47): Low survival probability
- **Charlotte Cardeza** (1st class female, age 58): High survival probability  
- **Bridget Delia** (3rd class female, age 30): Medium survival probability

## 🎯 Features

### Machine Learning Pipeline
- **Data Preprocessing**: Handles missing values, categorical encoding
- **Feature Engineering**: Age groups, fare categories, family size
- **Model Training**: Random Forest with cross-validation
- **Model Persistence**: Pickle serialization for deployment

### FastAPI Backend
- **RESTful API**: Clean endpoints for predictions
- **Health Monitoring**: System status and model validation
- **Data Validation**: Pydantic models for request/response
- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive exception management

### Java Frontend
- **Modern UI**: PrimeFaces components with responsive design
- **Form Validation**: Client and server-side validation
- **Sample Data**: Pre-loaded passenger examples for testing
- **Real-time Updates**: AJAX-powered interactions
- **Health Monitoring**: API status display

## 🔧 Technology Stack

### Backend Technologies
- **Python 3.8+**: Core language
- **FastAPI**: Modern web framework
- **Scikit-learn**: Machine learning library
- **Pandas**: Data manipulation
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend Technologies
- **Java 17**: Core language
- **Jakarta EE**: Enterprise Java platform
- **JSF 4.0**: JavaServer Faces framework
- **PrimeFaces 13.0**: UI component library
- **CDI**: Contexts and Dependency Injection
- **Maven**: Build automation

### Infrastructure
- **Tomcat 10**: Application server
- **Maven**: Dependency management
- **Git**: Version control

## 📊 Model Performance

The trained Random Forest model achieves:
- **Accuracy**: ~82% on test data
- **Features**: 8 engineered features from passenger data
- **Cross-validation**: 5-fold CV for robust evaluation

### Feature Importance
1. **Sex**: Most predictive feature
2. **Age**: Strong correlation with survival
3. **Fare**: Economic status indicator
4. **Passenger Class**: Social hierarchy
5. **Family Size**: SibSp + Parch

## 🎨 User Interface

### Key Components
- **Passenger Form**: Input validation with PrimeFaces components
- **Sample Passengers**: Quick-load examples for testing
- **Prediction Results**: Visual indicators with probabilities
- **API Health**: Real-time backend status monitoring

### Design Features
- **Responsive Layout**: Mobile-friendly design
- **Modern Styling**: Gradient backgrounds and smooth animations
- **User Feedback**: Success/error messages and loading states
- **Accessibility**: Semantic HTML and ARIA support

## 🔌 API Endpoints

### FastAPI Backend (`http://localhost:8000`)

```http
GET  /health                    # Health check
POST /predict                   # Single prediction
POST /predict/batch             # Batch predictions
GET  /docs                      # API documentation
```

### Example Request

```json
POST /predict
{
  "pclass": "1",
  "name": "Mr. John Doe",
  "sex": "male",
  "age": 35.0,
  "sibsp": 0,
  "parch": 0,
  "fare": 50.0,
  "embarked": "S"
}
```

### Example Response

```json
{
  "survived": 1,
  "survival_probability": 0.75,
  "death_probability": 0.25
}
```

## 🛠️ Development

### Running in Development Mode

1. **ML Model Development**:
   ```bash
   cd ml-model
   jupyter notebook notebooks/educational_content.ipynb
   ```

2. **API Development**:
   ```bash
   cd fastapi-backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Development**:
   ```bash
   cd java-frontend
   mvn clean compile
   mvn jetty:run
   ```

### Testing

- **Unit Tests**: Run `pytest` in the ML model directory
- **API Tests**: Use FastAPI's built-in test client
- **Integration Tests**: Manual testing through the web interface

## 📈 Performance Considerations

### Optimization Strategies
- **Model Caching**: Pre-loaded models for fast predictions
- **Connection Pooling**: Efficient HTTP client configuration
- **Async Processing**: Non-blocking API operations
- **Resource Management**: Proper cleanup of ML resources

### Scalability
- **Horizontal Scaling**: Stateless API design
- **Load Balancing**: Multiple API instances
- **Caching**: Redis for prediction results
- **Database**: PostgreSQL for production data

## 🔒 Security Considerations

- **Input Validation**: Comprehensive data sanitization
- **CORS Configuration**: Controlled cross-origin access
- **Error Handling**: Secure error messages
- **Dependency Management**: Regular security updates

## 🚀 Deployment

### Production Deployment

1. **Containerization**: Docker containers for each component
2. **Orchestration**: Kubernetes for container management
3. **Monitoring**: Health checks and metrics collection
4. **Logging**: Centralized log aggregation

### Environment Configuration

```bash
# Production environment variables
export ML_MODEL_PATH=/app/models
export API_HOST=0.0.0.0
export API_PORT=8000
export LOG_LEVEL=INFO
```

