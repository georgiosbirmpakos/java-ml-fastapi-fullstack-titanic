# Chatbot Service (LangChain + FastAPI)

This service accepts natural language descriptions of Titanic passengers, extracts a structured passenger using LangChain + OpenAI (gpt-4o-mini by default), and calls the existing FastAPI `/predict` endpoint to return survival predictions with reasoning.

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

## Notes
- Model can be configured via env var `OPENAI_MODEL` (default: gpt-4o-mini).
- RAG can be added later by augmenting `chains/` to retrieve Titanic background info.
- The Java frontend can call `http://localhost:8010/predict-nl` from the new AI Agent page.
