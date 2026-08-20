# PrepPath AI Backend Service

FastAPI-powered backend API for PrepPath AI (Opportunity-to-Application Readiness Platform).

## Directory Structure

```
backend/
├── app/
│   ├── main.py       # Application factory & CORS configuration
│   ├── config.py     # Pydantic Settings & Environment loading
│   ├── models/       # Database & Domain Models (Future phases)
│   ├── schemas/      # Pydantic Request/Response Schemas
│   ├── routes/       # API Routers & Endpoints
│   ├── services/     # Business & Deterministic Rule Engine Logic
│   ├── ai/           # AI Extraction & Explanation Handlers
│   └── utils/        # Common Utilities
├── requirements.txt  # Python Dependencies
└── README.md
```

## Setup & Running Locally

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # PowerShell / CMD
   .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Verify Health Endpoint**:
   - Access: `http://localhost:8000/health`
   - OpenAPI Documentation: `http://localhost:8000/docs`
