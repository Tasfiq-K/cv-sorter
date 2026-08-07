from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# Document Models
# ==========================================================


class CandidateDocument(BaseModel):
    """
    Represents an extracted CV document before parsing.
    """

    filename: str
    path: Path
    extension: str

    raw_text: str

    page_count: int = 0
    character_count: int = 0


class JobDescriptionDocument(BaseModel):
    """
    Represents an extracted Job Description before parsing.
    """

    filename: str
    path: Path
    extension: str

    raw_text: str

    page_count: int = 0
    character_count: int = 0


# ==========================================================
# Parsed Candidate
# ==========================================================


class CandidateProfile(BaseModel):
    """
    Structured information extracted from a CV.
    """
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    raw_text: str


# ==========================================================
# Parsed Job Description
# ==========================================================


class JobDescription(BaseModel):
    """
    Parsed job description.
    """

    title: Optional[str] = None
    company: Optional[str] = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: Optional[str] = None
    raw_text: str


# ==========================================================
# Score Models
# ==========================================================


class ScoreBreakdown(BaseModel):

    required_skill_score: float = 0.0
    preferred_skill_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0
    project_score: float = 0.0
    semantic_score: float = 0.0
    final_score: float = 0.0


class RankedCandidate(BaseModel):

    profile: CandidateProfile
    score: ScoreBreakdown
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)