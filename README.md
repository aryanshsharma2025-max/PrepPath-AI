# PrepPath AI

[![Backend Test Suite](https://img.shields.io/badge/Pytest-35%20Passing-10B981?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/aryanshsharma2025-max/PrepPath-AI)
[![FastAPI Backend](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://github.com/aryanshsharma2025-max/PrepPath-AI)
[![React Frontend](https://img.shields.io/badge/React%2018-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://github.com/aryanshsharma2025-max/PrepPath-AI)
[![Live UI Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://preppath-ai.vercel.app)

> **Opportunity-to-Application Readiness Platform**  
> Bridges scholarship discovery and application readiness through a dual-layer architecture: **LLM schema extraction** + **deterministic rule evaluation**.

---

## 📌 Core Engineering Philosophy

### *Eligibility ≠ Application Readiness*

A candidate may fulfill every formal eligibility criterion (e.g. minimum GPA, annual family income limit, domicile state) yet remain completely unready to apply due to missing income certificates, unverified caste affidavits, or short application deadlines.

To solve this without sacrificing reliability, PrepPath AI strictly enforces **zero-hallucination evaluation**:
- **LLMs (Google Gemini 2.5/Flash)** are utilized solely for *unstructured document parsing* and *schema extraction*.
- **Hard evaluation decisions** are executed exclusively by a *deterministic Python rule engine*.

---

## 🏗️ System Architecture & Data Flow

```
Scholarship Document (Official PDF)
                │
                ▼
 ┌────────────────────────────────────────────────────────┐
 │ 1. PDF Parsing Pipeline (PyMuPDF / pypdf)              │
 │    • Extracts raw text with size & page-count limits   │
 │    • Sanitizes multi-column and tabular layouts        │
 └────────────────────────────────────────────────────────┘
                │
                ▼
 ┌────────────────────────────────────────────────────────┐
 │ 2. Structured Schema Extraction (Gemini 2.5/Flash)    │
 │    • Enforces Pydantic OpportunityExtraction schema    │
 │    • Resolves criteria: age, income, marks, domicile   │
 │    • Identifies mandatory vs optional document list    │
 └────────────────────────────────────────────────────────┘
                │
                ▼
 ┌────────────────────────────────────────────────────────┐
 │ 3. Deterministic Rule Engine (Pure Python Engine)      │
 │    • Compares Student Profile vs Extracted Criteria    │
 │    • Strict Type Coercion (numeric thresholds, bools)  │
 │    • Flags: PASS | FAIL | UNKNOWN                      │
 └────────────────────────────────────────────────────────┘
                │
                ▼
 ┌────────────────────────────────────────────────────────┐
 │ 4. Readiness & Document Checklist Engine               │
 │    • Flags Missing Mandatory Documents                 │
 │    • Computes overall readiness status & action items  │
 └────────────────────────────────────────────────────────┘
```

---

## 🧪 Automated Test Suite (35 Passing Tests)

The backend maintains strict test coverage across business logic, PDF parsing edge cases, Pydantic schemas, and FastAPI HTTP endpoints.

```bash
cd backend
pytest tests/ -v
```

### Test Breakdown:
- **`tests/test_eligibility.py` (22 Tests)**:
  - Age threshold comparisons (`<`, `<=`, `>`, `>=`)
  - Family income limits with currency & separator cleaning
  - Academic percentage vs board percentile boundary handling
  - Domicile state, reservation categories, and BPL card verification
  - Attendance rate parsing (percentage vs qualitative compliance)
  - Missing field handling (correctly returns `UNKNOWN` instead of false rejection)
- **`tests/test_routes.py` (8 Tests)**:
  - `GET /health` and `GET /` root endpoints
  - `GET /api/profile` and `POST /api/profile` student profile updates
  - `POST /api/opportunities/analyze` input validation (non-PDF rejection, corrupted payload handling)
  - `POST /api/opportunities/{id}/eligibility` 404 handling and deterministic end-to-end evaluation
- **`tests/test_pdf.py` (3 Tests)**:
  - Valid text extraction, empty payload detection, and multi-page stream parsing
- **`tests/test_schemas.py` (2 Tests)**:
  - Pydantic model serialization and schema integrity

---

## 🛠️ Technology Stack

| Domain | Technology | Purpose |
|---|---|---|
| **Backend API** | Python 3.11+, FastAPI, Uvicorn | High-performance asynchronous REST API |
| **Validation & Data** | Pydantic v2 | Strict schema contracts and type coercion |
| **AI Extraction** | Google GenAI SDK (Gemini Flash) | Structured JSON criteria extraction from documents |
| **Document Processing** | PyMuPDF / pdfplumber | PDF stream extraction and page bounding |
| **Testing** | Pytest, FastAPI TestClient, AnyIO | Automated unit, route, and integration tests |
| **Frontend UI** | React 18, Vite, Tailwind CSS, Lucide | Modern dark-mode single-page interface |

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python `>= 3.11`
- Node.js `>= 18.0.0`
- Google Gemini API Key

### 1. Clone Repository
```bash
git clone https://github.com/aryanshsharma2025-max/PrepPath-AI.git
cd PrepPath-AI
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `backend/.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PROJECT_NAME="PrepPath AI API"
ALLOWED_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]
```

Run tests and start backend server:
```bash
pytest tests/
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 📊 Implementation Status & Roadmap

### ✅ Implemented & Tested
- [x] PyMuPDF / pypdf document ingestion pipeline
- [x] Google GenAI structured prompt engineering & Pydantic validation
- [x] Deterministic multi-variable rule evaluation engine
- [x] Student profile CRUD endpoints with fallback memory store
- [x] 35 automated Pytest unit and route integration tests
- [x] Responsive dark-mode React 18 / Tailwind CSS dashboard

### 🔄 Planned / Next Phase
- [ ] Cloud deployment of FastAPI backend microservice (Docker / Fly.io / Render)
- [ ] Supabase Auth OAuth session persistence
- [ ] Multi-document student credential vault for automated document matching

---

## 📄 License
MIT License.
