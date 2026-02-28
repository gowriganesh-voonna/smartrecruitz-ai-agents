# SmartRecruitz AI Agents – POC1
## Resume Parsing & Structured Profile Generation

---

# 1️⃣ Objective

Parse unstructured resume documents (PDF, DOCX, TXT, Image), extract structured candidate profile data, normalize skills to a standard taxonomy, compute domain-wise experience, and prepare the candidate profile for duplicate detection (POC2).

---

# 2️⃣ Expected Outcome

- Extract personal information
- Extract professional experience
- Identify domain per experience entry
- Compute domain-wise total experience
- Normalize skill variations (e.g., “JS” → “JavaScript”)
- Infer implied skills from context
- Assign proficiency levels per skill
- Return structured JSON candidate profile
- Achieve ≥ 95% extraction accuracy
- Ensure processing time < 15 seconds per resume

---

# 3️⃣ Official Input Format

```json
{

"candidate_id": "SR-2024-00123",
"resume_file": {
"file_path": "/uploads/resume_00123.pdf",
"file_type": "PDF",
"file_size_kb": 245,
"file_base64": "[base64_encoded_file]"
},
"extraction_config": {
"extract_skills": true,
"extract_experience": true,
"extract_education": true,
"extract_contact": true,
"extract_domain": true,
"extract_certifications": true,
"extract_projects": true,
"extract_languages": true
}

}
Note: File is sent directly to Claude AI.
AI reads PDF/DOCX/Image using vision
capabilities - no pre-processing needed
```

---

# 4️⃣ Official Output Format

```json
{
  "candidate_id": "SR-2024-00123",
  "parse_status": "SUCCESS" | "FAILED",
  "confidence_score": 0.94,
  "personal_info": {
    "full_name": "John Smith",
    "email": "john.smith@email.com",
    "phone": "+1-555-1234",
    "current_title": "Senior Software Engineer"
  },
  "experience": [
    {
      "company": "Tech Corp",
      "title": "Senior Developer",
      "start_date": "2020-01",
      "end_date": "2024-01",
      "duration_months": 48,
      "domain": "FinTech",
      "responsibilities": [
        "Built microservices using Python",
        "Led team of 5 developers"
      ],
      "is_current": true
    },
    {
      "company": "StartupXYZ",
      "title": "Software Engineer",
      "start_date": "2018-01",
      "end_date": "2020-01",
      "duration_months": 24,
      "domain": "E-Commerce",
      "responsibilities": [
        "Developed React applications"
      ]
    }
  ],
  "education": [
    {
      "institution": "State University",
      "degree": "BS",
      "field": "Computer Science",
      "graduation_year": 2018
    }
  ],
  "skills_raw": ["Python", "React", "AWS", "Docker"],
  "skills_normalized": [
    {
      "standard_name": "Python",
      "original_terms": ["Python"],
      "proficiency": "Advanced",
      "evidence": "4 years building microservices"
    },
    {
      "standard_name": "React",
      "original_terms": ["React"],
      "proficiency": "Intermediate",
      "evidence": "2 years frontend development"
    },
    {
      "standard_name": "AWS",
      "original_terms": ["AWS"],
      "proficiency": "Intermediate",
      "evidence": "Mentioned in Tech Corp role"
    }
  ],
  "implied_skills": [
    {
      "skill": "Microservices Architecture",
      "inferred_from": "Built microservices using Python",
      "confidence": 0.85
    },
    {
      "skill": "Team Leadership",
      "inferred_from": "Led team of 5 developers",
      "confidence": 0.90
    }
  ],
  "total_experience_years": 6,
  "primary_domain": "FinTech",
  "domain_wise_experience": [
    {
      "domain": "FinTech",
      "experience_years": 4,
      "experience_months": 48,
      "companies": ["Tech Corp"],
      "roles": ["Senior Developer"]
    },
    {
      "domain": "E-Commerce",
      "experience_years": 2,
      "experience_months": 24,
      "companies": ["StartupXYZ"],
      "roles": ["Software Engineer"]
    }
  ],
  "certifications": [
    {
      "name": "AWS Solutions Architect",
      "issuer": "Amazon Web Services",
      "year": 2022,
      "valid_until": "2025-06"
    }
  ],
  "projects": [
    {
      "name": "Payment Gateway Integration",
      "description": "Built payment processing system",
      "technologies": ["Python", "AWS", "PostgreSQL"],
      "domain": "FinTech"
    }
  ],
  "languages": [
    {"language": "English", "proficiency": "Native"},
    {"language": "Spanish", "proficiency": "Intermediate"}
  ],
  "parsing_warnings": [],
  "duplicate_pre_check": {
    "status": "NO_MATCH",
    "checked_fields": ["email", "phone"],
    "potential_matches": []
  },
  "storage": {
    "table": "candidates_staging",
    "candidate_status": "PENDING" | "DUPLICATE_REVIEW" | "MANUAL_REVIEW",
    "awaiting": "POC 2 - Deep Duplicate Analysis"
  }
}
```

Note : Extra sections should need to maintain.
```json
"extra_data": {
   "awards": [],
   "publications": [],
   "links": [],
   "others": []
}
```

---

# 5️⃣ Official Validation Rules

## HOW VALIDATION HAPPENS

| Validation Check            | Method                                             | Pass Criteria                                                                 |
|----------------------------|----------------------------------------------------|-------------------------------------------------------------------------------|
| Email Format               | Regex validation                                   | Valid email pattern (xxx@xxx.xxx)                                             |
| Phone Format               | Phone number parser library                        | Valid phone with country code                                                 |
| Date Consistency           | AI logic check                                     | End date > Start date, no future dates                                        |
| Experience Timeline        | AI validates no overlapping full-time jobs         | Logical timeline without conflicts                                            |
| Domain Classification      | AI domain identification + master list validation  | Domain mapped to standard taxonomy (FinTech, Healthcare, etc.)               |
| Domain Experience Sum      | Calculation validation                             | Sum of domain-wise experience = total experience                              |
| Quick Duplicate Pre-Check  | Exact match query on candidates_main (email, phone)| Flag if exact match found, proceed to staging regardless                     |
| Required Fields            | Schema validation (Pydantic)                       | Name, at least 1 experience or education                                      |
| Confidence Score           | AI self-assessment                                 | Score > 0.7 to auto-accept, else manual review                                |

**Validation Outcome:** If validation fails, profile is flagged for manual review with specific error messages.

---

# 6️⃣ Official Process Flow

```
PROCESS FLOW

[Resume Upload] → [Send to Claude AI (Vision)]
(PDF/DOCX/Image)
            ↓
[AI Reads & Extracts ALL Data]
(No external parser)
            ↓
[Extract Complete Profile]
    - Personal Info, Contact
    - Experience with Domain identification
    - Education, Certifications
    - Projects, Languages
    - Raw Skills
            ↓
[AI Identifies Domain per Experience]
    - Classify company/role to domain
    - Calculate domain-wise experience
    - Identify primary domain
            ↓
[AI Normalizes Skills]
    - Map variations to standard names
    - Calculate proficiency from context
    - Infer implied skills
            ↓
[Structured JSON Output]
(Complete Profile + Domain + Normalized Skills)
            ↓
[Validation]
            ↓

┌──────────────────────────────────────────────┐
│  QUICK DUPLICATE PRE-CHECK (Email/Phone)    │
│  Check candidates_main for exact match      │
└──────────────────────────────────────────────┘
                        ↓
            ┌───────────┴───────────┐
            ↓                       ↓
      [No Match Found]        [Potential Match Found]
            ↓                       ↓
    status: "PENDING"     status: "DUPLICATE_REVIEW"
            ↓                       ↓
            └───────────┬───────────┘
                        ↓
        [Save to candidates_staging table]
                        ↓
        [Trigger POC 2: Deep Duplicate Analysis]
```

---

# 7️⃣ Storage Logic

## Database Table: candidates_staging

### Status Values

- PENDING
- DUPLICATE_REVIEW
- MANUAL_REVIEW

### Confidence Threshold Logic

- If confidence_score ≥ 0.7 → Auto Accept (Status = PENDING)
- If confidence_score < 0.7 → MANUAL_REVIEW

---

# End of POC1 Specification
