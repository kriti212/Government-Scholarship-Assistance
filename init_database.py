"""
Create scholarship_portal.db with schema + seed scholarships.

Run once:
  python init_database.py

Output:
  scholarship_portal.db  (in the Frontend folder)
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "database" / "schema.sql"
DB_FILE = BASE_DIR / "scholarship_portal.db"

SCHOLARSHIPS = [
    {
        "id": "sch-001",
        "name": "National Means-cum-Merit Scholarship (NMMS)",
        "provider": "Ministry of Education, Govt. of India",
        "description": "For meritorious students from economically weaker sections in secondary school.",
        "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
        "allowed_education_levels": ["Secondary School (Class 10)"],
        "max_income_range": "₹2,50,000 - ₹5,00,000",
        "min_age": 12,
        "max_age": 18,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 12000,
    },
    {
        "id": "sch-002",
        "name": "Post-Matric Scholarship for SC Students",
        "provider": "Ministry of Social Justice & Empowerment",
        "description": "Financial assistance for SC students in post-matriculation courses.",
        "allowed_categories": ["SC"],
        "allowed_education_levels": [
            "Higher Secondary (Class 12)",
            "Undergraduate Degree (UG)",
            "Postgraduate Degree (PG)",
            "Diploma / Vocational Training",
        ],
        "max_income_range": "₹2,50,000 - ₹5,00,000",
        "min_age": 15,
        "max_age": 35,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 50000,
    },
    {
        "id": "sch-003",
        "name": "Post-Matric Scholarship for ST Students",
        "provider": "Ministry of Tribal Affairs",
        "description": "Support for ST students in recognized post-matriculation courses.",
        "allowed_categories": ["ST"],
        "allowed_education_levels": [
            "Higher Secondary (Class 12)",
            "Undergraduate Degree (UG)",
            "Postgraduate Degree (PG)",
            "Diploma / Vocational Training",
        ],
        "max_income_range": "₹2,50,000 - ₹5,00,000",
        "min_age": 15,
        "max_age": 35,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 50000,
    },
    {
        "id": "sch-004",
        "name": "Central Sector Scheme of Scholarships",
        "provider": "Ministry of Education",
        "description": "Merit-based scholarship for UG/PG students from low-income families.",
        "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
        "allowed_education_levels": [
            "Undergraduate Degree (UG)",
            "Postgraduate Degree (PG)",
        ],
        "max_income_range": "₹1,00,000 - ₹2,50,000",
        "min_age": 17,
        "max_age": 30,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 20000,
    },
    {
        "id": "sch-005",
        "name": "National Fellowship for OBC Students",
        "provider": "Ministry of Social Justice & Empowerment",
        "description": "Fellowship for OBC students pursuing Ph.D. / research.",
        "allowed_categories": ["OBC"],
        "allowed_education_levels": ["Ph.D. / Research Fellowship"],
        "max_income_range": "More than ₹8,00,000",
        "min_age": 21,
        "max_age": 40,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 31000,
    },
    {
        "id": "sch-006",
        "name": "Pre-Matric Scholarship for Students with Disabilities",
        "provider": "Department of Empowerment of Persons with Disabilities",
        "description": "For PwD students in Class 9 and 10 from families with limited income.",
        "allowed_categories": ["General", "OBC", "SC", "ST", "EWS"],
        "allowed_education_levels": ["Secondary School (Class 10)"],
        "max_income_range": "₹2,50,000 - ₹5,00,000",
        "min_age": 13,
        "max_age": 18,
        "pwd_only": 1,
        "min_disability_percentage": 40,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 8000,
    },
    {
        "id": "sch-007",
        "name": "PM Yasasvi Scholarship Scheme",
        "provider": "Ministry of Social Justice & Empowerment",
        "description": "For OBC and EWS students in Class 9 to 12.",
        "allowed_categories": ["OBC", "EWS"],
        "allowed_education_levels": [
            "Secondary School (Class 10)",
            "Higher Secondary (Class 12)",
        ],
        "max_income_range": "₹2,50,000 - ₹5,00,000",
        "min_age": 13,
        "max_age": 18,
        "pwd_only": 0,
        "min_disability_percentage": None,
        "application_url": "https://scholarships.gov.in",
        "amount_inr": 75000,
    },
]


def main() -> None:
    if DB_FILE.exists():
        DB_FILE.unlink()

    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript(schema_sql)

        conn.executemany(
            """
            INSERT INTO scholarships (
                id, name, provider, description,
                allowed_categories, allowed_education_levels,
                max_income_range, min_age, max_age,
                pwd_only, min_disability_percentage,
                application_url, amount_inr, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            [
                (
                    item["id"],
                    item["name"],
                    item["provider"],
                    item["description"],
                    json.dumps(item["allowed_categories"]),
                    json.dumps(item["allowed_education_levels"]),
                    item["max_income_range"],
                    item["min_age"],
                    item["max_age"],
                    item["pwd_only"],
                    item["min_disability_percentage"],
                    item["application_url"],
                    item["amount_inr"],
                )
                for item in SCHOLARSHIPS
            ],
        )

        scholarship_count = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]

    print(f"Created: {DB_FILE}")
    print(f"Scholarships seeded: {scholarship_count}")


if __name__ == "__main__":
    main()
