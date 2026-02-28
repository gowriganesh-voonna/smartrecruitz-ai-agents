# SmartRecruitz AI Agents
## POC1 – Production Architecture (Final Locked Version)

---

# 1️⃣ Project Structure
```
smartrecruitz-ai-agents/
├── src/
│   ├── agents/              # AI Agent workflows, LLM orchestration, prompt engineering, and structured output generation
│   ├── api/                 # FastAPI endpoints, request validation, response models, and route handlers
│   ├── core/                # Global configuration, centralized logging, custom exceptions, and application-level settings
│   │   ├── config.py        # Environment configuration management (env variables, constants, settings loader)
│   │   ├── logging.py       # Structured logging setup (formatters, handlers, log levels)
│   │   ├── exceptions.py    # Custom exception classes and standardized error responses
│   │
│   ├── db/                  # Database layer (connection management and ORM models)
│   │   ├── session.py       # Database session creation, engine configuration, and connection pooling
│   │   ├── models.py        # SQLAlchemy ORM models and table definitions
│   │
│   ├── services/            # Business orchestration layer coordinating extraction, validation, scoring, and storage
│   ├── tasks/               # Asynchronous background processing and distributed task management
│   │   ├── celery_app.py    # Celery configuration, worker setup, and background task initialization
│   │
│   ├── utils/               # Reusable helper utilities (file parsing, validators, normalization helpers, scoring logic)
│
├── tests/                   # Unit tests, integration tests, and workflow validation tests
├── .env                     # Environment variables (API keys, DB credentials, secret configs — not committed to repo)
├── requirements.txt         # Python dependencies and version locking for reproducible environments
└── README.md                # Project documentation, architecture overview, setup instructions, and usage guide
```


## ✅ This Structure Ensures

- Clean separation of responsibilities
- No cross-layer dependency violations
- Replaceable AI layer
- Production scalability

---

# 2️⃣ High-Level System Architecture
```
Client (Resume Upload)
↓
FastAPI (API Layer)
↓
Service Layer (Business Orchestration)
↓
Text Extraction Layer (Free Libraries)
↓
LLM Structuring (Gemini API)
↓
Validation Layer (Python)
↓
Confidence Scoring Engine
↓
Duplicate Pre-Check (Service Layer)
↓
PostgreSQL (candidates_staging)
↓
Trigger → POC2
```


---

# 3️⃣ Layer-by-Layer Architecture

---

## 🔹 1. API Layer (`src/api/`)

### Responsibility

- Accept resume uploads
- Validate input format
- Trigger background processing
- Return job status

### Endpoints
POST /api/v1/resume/upload
GET /api/v1/resume/{job_id}
GET /health

### Important Rule

> API layer contains **NO business logic**.
> It only calls:
>
> `ResumeService.process_resume()`

---

## 🔹 2. Service Layer (`src/services/`)

### Responsibility

- Orchestrate complete resume processing
- Coordinate extraction → validation → storage
- Perform duplicate pre-check
- Manage DB writes
- Handle confidence threshold logic

### Core Flow Inside Service

1. Receive uploaded file
2. Store temporarily
3. Detect file type
4. Call Text Extraction Utility
5. Send extracted text to LLM
6. Validate structured output
7. Calculate confidence score
8. Run duplicate pre-check (email/phone)
9. Assign storage status
10. Save to `candidates_staging`
11. Trigger POC2 event

---

## 🔹 3. Text Extraction Layer (`src/utils/`)

### File Handling Strategy

| File Type               | Extraction Method          |
|--------------------------|---------------------------|
| PDF (text)               | pdfplumber / PyMuPDF      |
| DOCX                     | python-docx               |
| TXT                      | Native Python reader      |
| Scanned PDF / Images     | PaddleOCR (preferred)     |

### Why PaddleOCR?

- Handles colored PDFs
- Supports multi-column layouts
- Better layout detection for structured resumes

---

## 🔹 4. LLM Structuring Layer (Gemini API)

### Responsibility

Convert raw extracted text → structured JSON

### Extract

- Personal info
- Experience
- Education
- Skills
- Certifications
- Projects
- Languages

### Perform

- Domain classification
- Skill normalization
- Proficiency inference
- Implied skill detection

### Prompt Rule

The model must:

- Ignore section headings
- Extract semantically
- Not depend on fixed labels

---

## 🔹 5. Domain Classification Strategy (Hybrid)

### Step 1

LLM assigns domain per experience.

### Step 2

Python validates against master taxonomy.
```
MASTER_DOMAIN_LIST = [
"FinTech",
"Healthcare",
"E-Commerce",
"EdTech",
"SaaS",
"Telecom",
"Manufacturing",
"Logistics",
"Retail",
"Banking",
etc
]

```


### If Mismatch

- Normalize to closest valid domain
- Add parsing warning
- Reduce confidence score

---

## 🔹 6. Date Normalization Engine

### Handles

- Year-only dates
- Month + year
- "Present"
- Duration-only descriptions
- Missing dates

### Policy

| Scenario            | Action               |
|---------------------|----------------------|
| Year only           | Convert to Jan–Dec   |
| "Present"           | Use current date     |
| Duration mentioned  | Ask AI to infer      |
| No date             | Reduce confidence    |
| Overlapping roles   | Validation failure   |

---

## 🔹 7. Validation Engine (9 Rules)

Validation is applied **AFTER extraction**.

| Check                   | Method            |
|--------------------------|------------------|
| Email format             | Regex            |
| Phone format             | Phone parser     |
| Date consistency         | Python logic     |
| Timeline overlap         | Custom checker   |
| Domain validation        | Taxonomy match   |
| Domain sum check         | Calculation      |
| Required fields          | Pydantic schema  |
| Duplicate pre-check      | DB query         |
| Confidence threshold     | Weighted logic   |

---

## 🔹 8. Confidence Score Engine (Hybrid Model)
```
confidence =
0.4 * extraction_confidence +
0.3 * validation_pass_ratio +
0.2 * completeness_score +
0.1 * domain_consistency_score
```


### Threshold Logic

| Score | Status         |
|-------|---------------|
| ≥ 0.7 | PENDING       |
| < 0.7 | MANUAL_REVIEW |

---

## 🔹 9. Duplicate Pre-Check Placement

This happens in **Service Layer**, NOT Agent.

### Query
```
SELECT * FROM candidates_main
WHERE email = ?
OR phone = ?
```


### Status Assignment

| Condition    | Status             |
|-------------|--------------------|
| No match    | PENDING            |
| Match found | DUPLICATE_REVIEW   |

Note : if something went wrong " MANUAL_REVIEW" with error message need to save
---

## 🔹 10. Database Design

### Table: `candidates_staging`

### Important Columns

- candidate_id
- parse_status
- confidence_score
- structured_profile   (JSONB)
- candidate_status
- awaiting
- created_at
- updated_at


Where:

### structured_profile contains:

- personal_info

- experience

- education

- skills

- domains

- certifications

- projects

- languages

- warnings

- extra_data

- duplicate_pre_check

This is clean, scalable, and future-proof.

---

# 4️⃣ Complete Processing Flow (Step-by-Step)

1. Resume Uploaded
2. File Type Identified
3. Text Extracted
4. Gemini Structuring
5. Domain Classification Validated
6. Date Normalization Applied
7. Validation Engine Executes (9 checks)
8. Confidence Score Calculated
9. Duplicate Pre-Check (DB)
10. Status Assigned
11. Save to `candidates_staging`
12. Trigger POC2

---

# 5️⃣ Architecture Principles Followed

✔ Clean Layered Architecture
✔ Agents do NOT access database
✔ Services manage business logic
✔ Replaceable AI layer
✔ Modular extraction engine
✔ Validation-driven design
✔ Confidence-based automation
✔ Manual review fallback
✔ Production-ready scalability
