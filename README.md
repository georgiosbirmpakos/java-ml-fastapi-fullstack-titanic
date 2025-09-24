# Titanic Survival Prediction System

A full-stack machine learning application that predicts passenger survival on the Titanic using historical data. The system consists of a Python ML model, FastAPI backend, and Java frontend with modern web technologies.

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

## 🚀 Quick Start

### Prerequisites

- **Java 17+** with Maven
- **Python 3.8+** with pip
- **Tomcat 10** (Jakarta EE compatible)
- **Git**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd test_project
```

### 2. Train the ML Model

```bash
cd ml-model
pip install -r requirements.txt
python train.py
```

### 3. Start the FastAPI Backend

```bash
cd fastapi-backend
pip install fastapi uvicorn scikit-learn pandas
python app.py
```

The API will be available at: `http://localhost:8000`

### 4. Build and Deploy Java Frontend

```bash
cd java-frontend
mvn clean package
```

Deploy the generated `target/titanic-1.0.0.war` to your Tomcat server.

Access the application at: `http://localhost:8080/titanic-1.0.0/`

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

## 📚 Educational Content

The project includes comprehensive educational materials:

- **Jupyter Notebooks**: Data analysis and model explanation
- **Code Documentation**: Inline comments and docstrings
- **API Documentation**: Interactive Swagger/OpenAPI docs
- **Architecture Diagrams**: System design documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Titanic Dataset**: Kaggle's famous machine learning dataset
- **PrimeFaces**: Excellent JSF component library
- **FastAPI**: Modern Python web framework
- **Scikit-learn**: Comprehensive machine learning library

## 📞 Support

For questions, issues, or contributions:

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: [your-email@example.com](mailto:your-email@example.com)

---

**Built with ❤️ using modern web technologies and machine learning best practices.**