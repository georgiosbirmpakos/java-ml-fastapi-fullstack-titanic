# Titanic Frontend - Java EE Application

A modern Java EE frontend application for the Titanic Survival Prediction system using JSF, PrimeFaces, and OkHttp.

## 🏗️ Architecture

- **Framework**: Jakarta EE (Java 17)
- **UI Framework**: JSF (JavaServer Faces) with PrimeFaces 10
- **Dependency Injection**: CDI (Contexts and Dependency Injection)
- **HTTP Client**: OkHttp for API communication
- **Build Tool**: Maven
- **Styling**: Custom CSS with modern design

## 📁 Project Structure

```
java-frontend/
├── src/main/java/com/titanic/
│   ├── model/                    # Data models
│   │   ├── Passenger.java       # Passenger data model
│   │   └── PredictionResult.java # Prediction result model
│   ├── service/                  # Business logic
│   │   └── TitanicApiService.java # API communication service
│   └── managedbean/              # JSF managed beans
│       └── TitanicPredictionBean.java # Main application bean
├── src/main/webapp/
│   ├── WEB-INF/
│   │   ├── web.xml              # Web application configuration
│   │   └── beans.xml            # CDI configuration
│   ├── resources/css/
│   │   └── titanic.css          # Custom styling
│   └── index.xhtml              # Main application page
├── pom.xml                      # Maven configuration
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

- **Java 17** or higher
- **Maven 3.6+**
- **FastAPI Backend** running on `http://localhost:8000`

### Installation & Setup

1. **Clone and Navigate**
   ```bash
   cd java-frontend
   ```

2. **Install Dependencies**
   ```bash
   mvn clean install
   ```

3. **Start the Application**
   ```bash
   mvn jetty:run
   ```

4. **Access the Application**
   - Open browser: `http://localhost:8080/titanic`
   - The application will be available at `/titanic` context path

### Development Mode

For development with auto-reload:
```bash
mvn jetty:run -Djetty.scanIntervalSeconds=10
```

## 🎯 Features

### Core Functionality
- **Passenger Data Input**: Comprehensive form for passenger information
- **Real-time Prediction**: Live survival prediction via API
- **Sample Data**: Pre-loaded sample passengers for testing
- **API Health Check**: Monitor backend API status
- **Responsive Design**: Mobile-friendly interface

### UI Components
- **PrimeFaces Components**: Modern, accessible UI components
- **Form Validation**: Client and server-side validation
- **Custom Styling**: Beautiful gradient-based design
- **Interactive Elements**: Smooth animations and transitions

### Technical Features
- **CDI Integration**: Dependency injection for services
- **Error Handling**: Comprehensive error management
- **Logging**: SLF4J with Logback for application logging
- **Validation**: Bean validation with custom messages

## 🔧 Configuration

### API Configuration
The API endpoint is configured in `TitanicApiService.java`:
```java
private static final String API_BASE_URL = "http://localhost:8000";
```

### PrimeFaces Theme
Configured in `web.xml`:
```xml
<context-param>
    <param-name>primefaces.THEME</param-name>
    <param-value>nova-light</param-value>
</context-param>
```

### Development Settings
- **Project Stage**: Development (enables debug features)
- **Facelets Refresh**: 1 second (for development)
- **Client-side Validation**: Enabled

## 📱 User Interface

### Main Components

1. **API Status Panel**
   - Real-time API health monitoring
   - Connection status display
   - Manual health check button

2. **Passenger Form**
   - Passenger class selection (1st, 2nd, 3rd)
   - Name input with validation
   - Sex selection (Male/Female)
   - Age, siblings, parents, fare inputs
   - Embarkation port selection

3. **Sample Passengers**
   - Pre-loaded historical passengers
   - One-click loading for testing
   - Real Titanic passenger data

4. **Prediction Results**
   - Visual survival/dearth indicators
   - Probability percentages
   - Color-coded results

### Responsive Design
- **Desktop**: Two-column layout with side-by-side panels
- **Mobile**: Single-column stacked layout
- **Tablet**: Adaptive grid system

## 🛠️ Development

### Adding New Features

1. **New Model Classes**
   ```java
   @Data
   @NoArgsConstructor
   @AllArgsConstructor
   public class NewModel implements Serializable {
       // Fields with validation annotations
   }
   ```

2. **New Services**
   ```java
   @ApplicationScoped
   public class NewService {
       // Business logic
   }
   ```

3. **New Managed Beans**
   ```java
   @Named("newBean")
   @ViewScoped
   public class NewBean implements Serializable {
       @Inject
       private NewService service;
       // UI logic
   }
   ```

### Styling Guidelines

- Use CSS Grid and Flexbox for layouts
- Implement gradient backgrounds for visual appeal
- Use consistent color scheme:
  - Primary: `#3498db`
  - Success: `#27ae60`
  - Warning: `#f39c12`
  - Danger: `#e74c3c`
- Add smooth transitions for interactive elements

## 🧪 Testing

### Manual Testing
1. **API Connection**: Verify API health check works
2. **Form Validation**: Test all validation rules
3. **Sample Data**: Load and predict with sample passengers
4. **Responsive Design**: Test on different screen sizes

### Sample Test Cases
- **John Astor** (1st class male): Should show low survival probability
- **Charlotte Cardeza** (1st class female): Should show high survival probability
- **Bridget Delia** (3rd class female): Should show medium survival probability

## 🚀 Deployment

### Production Build
```bash
mvn clean package
```

### WAR File Location
```
target/titanic-frontend-1.0.0.war
```

### Application Server Deployment
1. Deploy WAR file to your application server
2. Configure context path if needed
3. Update API URL for production environment
4. Configure logging levels

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure FastAPI backend is running on port 8000
   - Check firewall settings
   - Verify API health endpoint

2. **CDI Not Working**
   - Ensure `beans.xml` is present in WEB-INF
   - Check CDI implementation (Weld) is included
   - Verify `@Named` and `@Inject` annotations

3. **PrimeFaces Components Not Rendering**
   - Check PrimeFaces dependency in pom.xml
   - Verify theme configuration
   - Ensure proper namespace declarations

4. **Validation Not Working**
   - Check validation annotations
   - Verify Hibernate Validator dependency
   - Ensure proper error message configuration

### Logs
Application logs are available in the console output. Key loggers:
- `com.titanic.service.TitanicApiService`
- `com.titanic.managedbean.TitanicPredictionBean`

## 📚 Educational Content

See `notebooks/educational_content.ipynb` for comprehensive learning materials covering:
- Java EE architecture
- JSF development
- PrimeFaces components
- CDI and dependency injection
- HTTP client integration
- Best practices

## 🤝 Contributing

1. Follow Java coding standards
2. Use Lombok for model classes
3. Add proper validation annotations
4. Include comprehensive logging
5. Test on multiple browsers
6. Ensure responsive design

## 📄 License

This project is part of the Titanic Survival Prediction educational project.
