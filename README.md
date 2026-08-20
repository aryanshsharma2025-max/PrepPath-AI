# PrepPath AI

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://preppath-ai.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-PrepPath--AI-blue?style=for-the-badge&logo=github)](https://github.com/aryanshsharma2025-max/PrepPath-AI)

> 🌐 **Live Website:** [https://preppath-ai.vercel.app](https://preppath-ai.vercel.app)  
> **From Opportunity to Application-Ready**

PrepPath AI is an AI-powered **Opportunity-to-Application Readiness** platform. While the initial MVP focuses specifically on **Scholarships**, the system architecture is designed from the ground up to be extensible for future opportunity types including internships, competitions, fellowships, and government schemes.

---

## Core Product Principle

**Eligibility and readiness are NOT the same thing.**

A student can meet all formal eligibility criteria for an opportunity but still be completely unready to apply due to missing documents, incomplete profile fields, or tight deadlines. 

PrepPath AI evaluates four distinct dimensions:
1. **Eligibility**: Does the candidate satisfy hard rules and constraints?
2. **Application Readiness**: Does the candidate possess all required documents and structured profile data?
3. **Application Risk**: What inconsistencies, gaps, or deadlines pose a threat to application success?
4. **Next Best Action**: Clear, prioritized steps to bridge readiness gaps.

---

## AI & Rule Engine Architecture

To guarantee accuracy and eliminate hallucinated eligibility decisions, PrepPath AI enforces strict separation between decision logic and AI explanations:

```
Opportunity Document (PDF / URL)
           ↓
     AI Extraction
           ↓
 Structured Requirements
           ↓
 Deterministic Rule Engine  <--- Decision Maker
           ↓
     Eligibility Result
           ↓
  AI-Generated Explanation  <--- Explainer & Assistant
```

- **Rule Engine**: Evaluates criteria deterministically.
- **AI (Gemini)**: Extracts structured criteria and provides user assistance, document insights, and clear explanations.

---

## Technical Architecture & Stack

- **Frontend**: React, Vite, JavaScript, Tailwind CSS
- **Backend**: Python, FastAPI, Uvicorn
- **Database**: Supabase PostgreSQL *(Future Phase)*
- **Authentication**: Supabase Auth *(Future Phase)*
- **Storage**: Supabase Storage *(Future Phase)*
- **AI**: Gemini API *(Future Phase)*
- **PDF Processing**: PyMuPDF *(Future Phase)*

---

## Project Structure

```
PrepPath-AI/
├── frontend/             # React + Vite + Tailwind CSS User Interface
│   ├── src/
│   │   ├── components/   # Reusable UI Components
│   │   ├── pages/        # Route / Screen Components
│   │   ├── layouts/      # Application Layout Shells
│   │   ├── services/     # API Integration Layer
│   │   ├── hooks/        # Custom React Hooks
│   │   ├── utils/        # Helper Utilities
│   │   └── App.jsx       # Root Application Component
│   ├── package.json
│   └── README.md
│
├── backend/              # FastAPI Python Service
│   ├── app/
│   │   ├── main.py       # FastAPI Entrypoint & CORS setup
│   │   ├── config.py     # Environment & Application Settings
│   │   ├── models/       # Data Models & Entities
│   │   ├── schemas/      # Pydantic Schemas & DTOs
│   │   ├── routes/       # API Endpoint Routers
│   │   ├── services/     # Business Logic & Deterministic Engine
│   │   ├── ai/           # Gemini AI Extraction & Explanation Services
│   │   └── utils/        # Shared Utilities
│   ├── requirements.txt
│   └── README.md
│
├── docs/                 # Product Specifications & Architecture Docs
├── data/                 # Sample Data & Opportunity Fixtures
├── .env.example          # Environment Variable Templates
└── README.md
```

---

## Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell / CMD:
.venv\Scripts\activate
pip install -r requirements.txt

# Run FastAPI Server
uvicorn app.main:app --reload --port 8000
```
- API Health Check: `http://localhost:8000/health`
- OpenAPI Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

## Initial Health Endpoint Specification

- **`GET /health`**
  - **Response**:
    ```json
    {
      "status": "healthy",
      "service": "PrepPath AI API"
    }
    ```

---

## License

Private & Confidential - PrepPath AI MVP.
