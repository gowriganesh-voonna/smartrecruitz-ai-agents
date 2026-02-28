# 🚀 FINAL PHASE-WISE DEVELOPMENT PLAN (LOCKED)

---

## 🔵 Phase 1 – Foundation Setup (Infrastructure Ready)

### Objective:
Establish system backbone before writing business logic.

### Tasks:
- PostgreSQL schema creation (`candidates_staging`)
- SQLAlchemy ORM models
- Core configuration module (`config.py`)
- Environment variable management (`.env`)
- Logging framework (structlog JSON logging)
- Exception handling module

### Output of Phase 1:
- DB ready
- Config ready
- Logging ready
- Project runs without business logic

### Meeting Statement:
> Phase 1 establishes the infrastructure layer including database schema, configuration management, logging framework, and environment setup.

---

## 🔵 Phase 2 – API & Service Orchestration

### Objective:
Build entry point and orchestration flow.

### Tasks:
- Implement `POST /resume/upload`
- Implement `GET /resume/{job_id}`
- Implement service layer orchestration (`ResumeService`)
- Temporary file storage handling
- Background processing trigger

### Flow Designed (No logic yet):
Upload → Store file → Call ResumeService → Return job_id

### Output:
- API functional
- Job tracking working
- No extraction yet

### Meeting Statement:
> Phase 2 establishes API endpoints and orchestrates the high-level processing flow without implementing extraction logic yet.

---

## 🔵 Phase 3 – File Processing Engine

### Objective:
Extract clean raw text from any resume format.

### Tasks:
- PDF text extraction (`pdfplumber` / `PyMuPDF`)
- DOCX extraction (`python-docx`)
- TXT reader
- PaddleOCR integration (for scanned/image resumes)
- File type auto-detection
- Light cleaning (whitespace, encoding fixes)

### Important:
No AI yet in this phase.

### Output:
Raw clean text extracted reliably.

### Meeting Statement:
> Phase 3 implements the file processing engine to handle multiple resume formats including scanned and structured documents.

---

## 🔵 Phase 4 – AI Structuring Engine (Gemini Integration)

### Objective:
Convert raw text → structured JSON.

### Tasks:
- Gemini API integration
- Strict extraction prompt design
- Domain classification via AI
- Skill normalization via AI
- Proficiency inference
- Implied skills extraction
- JSON parsing validation (Pydantic enforcement)

### Removed:
- ❌ Claude fallback
- ❌ Separate JSON repair agent

### Output:
Structured candidate profile (raw AI output).

### Meeting Statement:
> Phase 4 integrates Gemini for semantic structuring, domain classification, and skill normalization.

---

## 🔵 Phase 5 – Normalization & Data Integrity Layer

### Objective:
Enforce structural consistency before validation.

### Tasks:
- Master domain taxonomy validation
- Domain normalization mapping
- Date normalization logic
- Experience duration calculation
- Overlap detection utility
- Missing date handling policy

**Note:** This is Python logic, not AI.

### Output:
Clean, normalized structured profile.

### Meeting Statement:
> Phase 5 ensures domain consistency, date normalization, and structural integrity before validation.

---

## 🔵 Phase 6 – Validation & Confidence Scoring

### Objective:
Apply official 9-rule validation.

### Tasks:
- Email regex validation
- Phone parser validation
- Date consistency validation
- Timeline overlap validation
- Domain experience sum validation
- Required fields validation
- Duplicate pre-check (DB query)
- Weighted confidence scoring model

### Output:
Final profile with:
- `parse_status`
- `confidence_score`
- `candidate_status`

### Meeting Statement:
> Phase 6 applies the official 9 validation rules and computes a weighted confidence score governing automation vs manual review.

---

## 🔵 Phase 7 – Storage & Event Integration

### Objective:
Persist and trigger next system.

### Tasks:
- Insert into `candidates_staging`
- Assign `candidate_status`:
  - `PENDING`
  - `DUPLICATE_REVIEW`
  - `MANUAL_REVIEW`
- Store `structured_profile` (JSONB)
- Trigger POC2 event (Kafka / internal call)

### Meeting Statement:
> Phase 7 handles final persistence and initiates duplicate detection workflow (POC2).

---

## 🔵 Phase 8 – Testing & Hardening

### Objective:
Make system production-ready.

### Tasks:
- Unit tests (≥ 90% coverage)
- Integration tests (upload → DB flow)
- Invalid resume testing
- Missing data testing
- Duplicate simulation
- Performance testing (< 15 sec target)
- Load testing
- Logging audit verification

### Meeting Statement:
> Phase 8 focuses on stability, reliability, performance validation, and production hardening.

---

# 📊 FINAL PHASE SUMMARY TABLE

| Phase   | Layer Focus                    |
|---------|--------------------------------|
| Phase 1 | Infrastructure                 |
| Phase 2 | API & Orchestration            |
| Phase 3 | File Processing                |
| Phase 4 | AI Structuring                 |
| Phase 5 | Normalization                  |
| Phase 6 | Validation & Scoring           |
| Phase 7 | Storage & Integration          |
| Phase 8 | Testing & Hardening            |
