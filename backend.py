"""
Scholarship Eligibility Portal — single-file backend
Matches the Streamlit frontend form fields in app.py

Run:
  pip install fastapi uvicorn pydantic
  uvicorn backend:app --reload --host 127.0.0.1 --port 8000

API docs: http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Schemas (aligned with frontend selectbox / radio options)
# ---------------------------------------------------------------------------

Gender = Literal["Male", "Female", "Other", "Prefer not to say"]
Category = Literal["General", "OBC", "SC", "ST", "EWS"]
EducationLevel = Literal[
    "Secondary School (Class 10)",
    "Higher Secondary (Class 12)",
    "Undergraduate Degree (UG)",
    "Postgraduate Degree (PG)",
    "Ph.D. / Research Fellowship",
    "Diploma / Vocational Training",
]
IncomeRange = Literal[
    "Less than ₹1,00,000",
    "₹1,00,000 - ₹2,50,000",
    "₹2,50,000 - ₹5,00,000",
    "₹5,00,000 - ₹8,00,000",
    "More than ₹8,00,000",
]
DisabilityType = Literal[
    "Locomotor Disability",
    "Visual Impairment",
    "Hearing Impairment",
    "Speech and Language Disability",
    "Intellectual Disability / Autism",
    "Multiple Disabilities",
]

INCOME_ORDER: list[IncomeRange] = [
    "Less than ₹1,00,000",
    "₹1,00,000 - ₹2,50,000",
    "₹2,50,000 - ₹5,00,000",
    "₹5,00,000 - ₹8,00,000",
    "More than ₹8,00,000",
]


class CandidateRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    age: int = Field(..., ge=5, le=100)
    gender: Gender
    caste: Category
    education_level: EducationLevel
    income_range: IncomeRange
    is_disabled: bool = False
    disability_type: DisabilityType | None = None
    disability_percentage: int | None = Field(default=None, ge=40, le=100)

    @field_validator("full_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Full name cannot be empty.")
        return cleaned

    @model_validator(mode="after")
    def validate_disability(self) -> CandidateRegisterRequest:
        if self.is_disabled:
            if self.disability_type is None:
                raise ValueError("disability_type is required when is_disabled is true.")
            if self.disability_percentage is None:
                self.disability_percentage = 40
        else:
            self.disability_type = None
            self.disability_percentage = None
        return self


class Scholarship(BaseModel):
    id: str
    name: str
    provider: str
    description: str
    allowed_categories: list[Category]
    allowed_education_levels: list[EducationLevel]
    max_income_range: IncomeRange
    min_age: int | None = None
    max_age: int | None = None
    pwd_only: bool = False
    min_disability_percentage: int | None = None
    application_url: str
    amount_inr: int | None = None


class CandidateRecord(CandidateRegisterRequest):
    id: str
    created_at: str


class RegisterResponse(BaseModel):
    message: str
    candidate: CandidateRecord
    eligible_scholarships: list[Scholarship]
    total_matches: int


# ---------------------------------------------------------------------------
# Scholarship catalog (same rules your frontend form is designed for)
# ---------------------------------------------------------------------------

SCHOLARSHIPS: list[Scholarship] = [
    Scholarship(
        id="sch-001",
        name="National Means-cum-Merit Scholarship (NMMS)",
        provider="Ministry of Education, Govt. of India",
        description="For meritorious students from economically weaker sections in secondary school.",
        allowed_categories=["General", "OBC", "SC", "ST", "EWS"],
        allowed_education_levels=["Secondary School (Class 10)"],
        max_income_range="₹2,50,000 - ₹5,00,000",
        min_age=12,
        max_age=18,
        application_url="https://scholarships.gov.in",
        amount_inr=12000,
    ),
    Scholarship(
        id="sch-002",
        name="Post-Matric Scholarship for SC Students",
        provider="Ministry of Social Justice & Empowerment",
        description="Financial assistance for SC students in post-matriculation courses.",
        allowed_categories=["SC"],
        allowed_education_levels=[
            "Higher Secondary (Class 12)",
            "Undergraduate Degree (UG)",
            "Postgraduate Degree (PG)",
            "Diploma / Vocational Training",
        ],
        max_income_range="₹2,50,000 - ₹5,00,000",
        min_age=15,
        max_age=35,
        application_url="https://scholarships.gov.in",
        amount_inr=50000,
    ),
    Scholarship(
        id="sch-003",
        name="Post-Matric Scholarship for ST Students",
        provider="Ministry of Tribal Affairs",
        description="Support for ST students in recognized post-matriculation courses.",
        allowed_categories=["ST"],
        allowed_education_levels=[
            "Higher Secondary (Class 12)",
            "Undergraduate Degree (UG)",
            "Postgraduate Degree (PG)",
            "Diploma / Vocational Training",
        ],
        max_income_range="₹2,50,000 - ₹5,00,000",
        min_age=15,
        max_age=35,
        application_url="https://scholarships.gov.in",
        amount_inr=50000,
    ),
    Scholarship(
        id="sch-004",
        name="Central Sector Scheme of Scholarships",
        provider="Ministry of Education",
        description="Merit-based scholarship for UG/PG students from low-income families.",
        allowed_categories=["General", "OBC", "SC", "ST", "EWS"],
        allowed_education_levels=["Undergraduate Degree (UG)", "Postgraduate Degree (PG)"],
        max_income_range="₹1,00,000 - ₹2,50,000",
        min_age=17,
        max_age=30,
        application_url="https://scholarships.gov.in",
        amount_inr=20000,
    ),
    Scholarship(
        id="sch-005",
        name="National Fellowship for OBC Students",
        provider="Ministry of Social Justice & Empowerment",
        description="Fellowship for OBC students pursuing Ph.D. / research.",
        allowed_categories=["OBC"],
        allowed_education_levels=["Ph.D. / Research Fellowship"],
        max_income_range="More than ₹8,00,000",
        min_age=21,
        max_age=40,
        application_url="https://scholarships.gov.in",
        amount_inr=31000,
    ),
    Scholarship(
        id="sch-006",
        name="Pre-Matric Scholarship for Students with Disabilities",
        provider="Department of Empowerment of Persons with Disabilities",
        description="For PwD students in Class 9 and 10 from families with limited income.",
        allowed_categories=["General", "OBC", "SC", "ST", "EWS"],
        allowed_education_levels=["Secondary School (Class 10)"],
        max_income_range="₹2,50,000 - ₹5,00,000",
        min_age=13,
        max_age=18,
        pwd_only=True,
        min_disability_percentage=40,
        application_url="https://scholarships.gov.in",
        amount_inr=8000,
    ),
    Scholarship(
        id="sch-007",
        name="PM Yasasvi Scholarship Scheme",
        provider="Ministry of Social Justice & Empowerment",
        description="For OBC and EWS students in Class 9 to 12.",
        allowed_categories=["OBC", "EWS"],
        allowed_education_levels=[
            "Secondary School (Class 10)",
            "Higher Secondary (Class 12)",
        ],
        max_income_range="₹2,50,000 - ₹5,00,000",
        min_age=13,
        max_age=18,
        application_url="https://scholarships.gov.in",
        amount_inr=75000,
    ),
]

# ---------------------------------------------------------------------------
# SQLite persistence (created next to this file)
# ---------------------------------------------------------------------------

DB_PATH = Path(__file__).resolve().parent / "candidates.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                caste TEXT NOT NULL,
                education_level TEXT NOT NULL,
                income_range TEXT NOT NULL,
                is_disabled INTEGER NOT NULL,
                disability_type TEXT,
                disability_percentage INTEGER,
                created_at TEXT NOT NULL
            )
            """
        )


def save_candidate(payload: CandidateRegisterRequest) -> CandidateRecord:
    candidate_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO candidates (
                id, full_name, age, gender, caste, education_level,
                income_range, is_disabled, disability_type, disability_percentage, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                candidate_id,
                payload.full_name,
                payload.age,
                payload.gender,
                payload.caste,
                payload.education_level,
                payload.income_range,
                int(payload.is_disabled),
                payload.disability_type,
                payload.disability_percentage,
                created_at,
            ),
        )

    return CandidateRecord(id=candidate_id, created_at=created_at, **payload.model_dump())


def get_candidate(candidate_id: str) -> CandidateRecord | None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,)).fetchone()

    if row is None:
        return None

    return CandidateRecord(
        id=row["id"],
        full_name=row["full_name"],
        age=row["age"],
        gender=row["gender"],
        caste=row["caste"],
        education_level=row["education_level"],
        income_range=row["income_range"],
        is_disabled=bool(row["is_disabled"]),
        disability_type=row["disability_type"],
        disability_percentage=row["disability_percentage"],
        created_at=row["created_at"],
    )


# ---------------------------------------------------------------------------
# Eligibility engine
# ---------------------------------------------------------------------------


def income_within_limit(candidate_income: IncomeRange, scholarship_max: IncomeRange) -> bool:
    return INCOME_ORDER.index(candidate_income) <= INCOME_ORDER.index(scholarship_max)


def is_eligible(scholarship: Scholarship, candidate: CandidateRegisterRequest) -> bool:
    if scholarship.min_age is not None and candidate.age < scholarship.min_age:
        return False
    if scholarship.max_age is not None and candidate.age > scholarship.max_age:
        return False
    if candidate.caste not in scholarship.allowed_categories:
        return False
    if candidate.education_level not in scholarship.allowed_education_levels:
        return False
    if not income_within_limit(candidate.income_range, scholarship.max_income_range):
        return False

    if scholarship.pwd_only:
        if not candidate.is_disabled:
            return False
        if (
            scholarship.min_disability_percentage is not None
            and (candidate.disability_percentage or 0) < scholarship.min_disability_percentage
        ):
            return False

    return True


def find_eligible_scholarships(candidate: CandidateRegisterRequest) -> list[Scholarship]:
    return [item for item in SCHOLARSHIPS if is_eligible(item, candidate)]


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Scholarship Eligibility Portal API",
    description="Backend for the Streamlit Candidate Registration Portal",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "Scholarship Eligibility Portal API"}


@app.get("/api/v1/scholarships", response_model=list[Scholarship])
def list_scholarships() -> list[Scholarship]:
    return SCHOLARSHIPS


@app.post("/api/v1/candidates/register", response_model=RegisterResponse)
def register_candidate(payload: CandidateRegisterRequest) -> RegisterResponse:
    saved = save_candidate(payload)
    matches = find_eligible_scholarships(payload)

    return RegisterResponse(
        message="Profile registered successfully.",
        candidate=saved,
        eligible_scholarships=matches,
        total_matches=len(matches),
    )


@app.get("/api/v1/candidates/{candidate_id}/eligibility")
def get_eligibility(candidate_id: str) -> dict:
    candidate = get_candidate(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    matches = find_eligible_scholarships(candidate)
    return {
        "candidate_id": candidate_id,
        "eligible_scholarships": matches,
        "total_matches": len(matches),
    }
