# AI Chatbot Service (LangChain + FastAPI + OpenAI)

This service provides an AI-powered chatbot that accepts natural language descriptions of Titanic passengers, extracts structured passenger data using OpenAI GPT-4o mini and LangChain, and calls the existing FastAPI `/predict` endpoint to return survival predictions with detailed explanations.

## 🚀 Features

- **Natural Language Processing**: OpenAI GPT-4o mini integration
- **Structured Data Extraction**: LangChain-based passenger data parsing
- **Manual Fallback Rules**: Regex-based extraction for reliability
- **FastAPI Integration**: Seamless communication with ML backend
- **Health Monitoring**: Built-in health checks and status endpoints
- **Docker Ready**: Full containerization support

## Quick Start (Local)

1. Create env file
```
cd chatbot-service
copy .env.example .env  # Windows
# or: cp .env.example .env
# Fill OPENAI_API_KEY
```

2. Install deps
```
pip install -r requirements.txt
```

3. Run service
```
uvicorn app:app --reload --port 8010
```

4. Ensure the existing backend is running
```
cd ../fastapi-backend
python app.py
```

5. Test
```
curl -X POST http://127.0.0.1:8010/predict-nl \
  -H "Content-Type: application/json" \
  -d '{"message": "Mr. John Doe, male, 35 years old, 1st class, fare 50, embarked at S"}'
```

## 🐳 Docker Integration

The chatbot service is fully integrated into the Docker ecosystem:

```bash
# Start all services including chatbot
docker-compose up -d

# Access chatbot API
curl http://localhost:8010/test
```

## 📊 API Endpoints

- `GET /test` - Health check endpoint
- `GET /health` - Service health status
- `POST /predict-nl` - Natural language prediction endpoint
- `GET /docs` - Interactive API documentation

## 🔧 Configuration

- **OpenAI Model**: Configurable via `OPENAI_MODEL` env var (default: gpt-4o-mini)
- **API Key**: Required `OPENAI_API_KEY` environment variable
- **Backend URL**: Configurable via `FASTAPI_BASE_URL` (default: http://fastapi-backend:8000)

## 🎯 Usage Examples

### Natural Language Input:
```
"A young woman, 22 years old, third class passenger from Ireland traveling with her family. She paid 7 pounds for her ticket."
```

### Expected Output:
```json
{
  "passenger": {
    "pclass": 3,
    "name": "Unknown Passenger",
    "sex": "female",
    "age": 22.0,
    "sibsp": 0,
    "parch": 2,
    "fare": 7.0,
    "embarked": "S"
  },
  "survived": 1,
  "survival_probability": 0.78,
  "death_probability": 0.22,
  "reasoning": "Extracted passenger information from natural language",
  "discussion": "Detailed explanation of the prediction..."
}
```

## 🛡️ Robustness Features

- **Manual Extraction Fallback**: Regex-based rules for when AI fails
- **Error Handling**: Comprehensive exception management
- **Validation**: Pydantic models for data validation
- **Logging**: Detailed request/response logging for debugging
