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


# ============================================================================
# Contact Information
# ============================================================================


class ContactInfo(BaseModel):

    email: str | None = None
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None


# ============================================================================
# Education
# ============================================================================


class EducationEntry(BaseModel):
    """
    Exactly as extracted by the LLM.

    No normalization happens here.
    """

    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    grade: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    description: str | None = None


# ============================================================================
# Experience
# ============================================================================


class ExperienceEntry(BaseModel):
    """
    Raw employment history.

    Dates remain exactly as written in the CV.
    """

    company: str | None = None
    role: str | None = None
    employment_type: str | None = None
    location: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    currently_working: bool | None = None
    technologies: list[str] = Field(default_factory=list)
    description: str | None = None


# ============================================================================
# Projects
# ============================================================================


class ProjectEntry(BaseModel):

    title: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)
    github: str | None = None
    demo: str | None = None


# ============================================================================
# Certifications
# ============================================================================


class CertificationEntry(BaseModel):

    name: str | None = None
    issuer: str | None = None
    issue_date_raw: str | None = None


# ============================================================================
# Skills
# ============================================================================


class SkillEntry(BaseModel):

    name: str
    category: str | None = None


# ============================================================================
# Languages
# ============================================================================


class LanguageEntry(BaseModel):

    name: str
    proficiency: str | None = None


# ============================================================================
# Parsed Resume
# ============================================================================


class CandidateProfile(BaseModel):
    """
    Structured resume returned by the LLM.

    This model intentionally stores extracted facts only.
    No derived information belongs here.
    """

    name: str | None = None
    headline: str | None = None
    summary: str | None = None
    contact: ContactInfo = Field(default_factory=ContactInfo)
    skills: list[SkillEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    projects: list[ProjectEntry] = Field(default_factory=list)
    certifications: list[CertificationEntry] = Field(default_factory=list)
    languages: list[LanguageEntry] = Field(default_factory=list)
    raw_text: str


# ============================================================================
# Parsed Job Description
# ============================================================================


class JobDescription(BaseModel):
    """
    Structured Job Description returned by the LLM.
    """

    title: str | None = None
    company: str | None = None
    location: str | None = None
    employment_type: str | None = None
    summary: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    required_education: list[str] = Field(default_factory=list)
    preferred_education: list[str] = Field(default_factory=list)
    required_certifications: list[str] = Field(default_factory=list)
    preferred_certifications: list[str] = Field(default_factory=list)
    experience_requirement: str | None = None
    raw_text: str


# ============================================================================
# Derived Features
# ============================================================================


class CandidateFeatures(BaseModel):
    """
    Generated AFTER parsing.

    Everything here is deterministic and calculated
    from CandidateProfile.
    """

    total_experience_months: int = 0
    relevant_experience_months: int = 0
    internship_count: int = 0
    project_count: int = 0
    certification_count: int = 0
    highest_degree: str | None = None
    normalized_skills: list[str] = Field(default_factory=list)


# ============================================================================
# Scoring
# ============================================================================


class ScoreBreakdown(BaseModel):

    required_skill_score: float = 0.0
    preferred_skill_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0
    project_score: float = 0.0
    certification_score: float = 0.0
    semantic_score: float = 0.0
    final_score: float = 0.0


class RankedCandidate(BaseModel):

    profile: CandidateProfile
    features: CandidateFeatures
    score: ScoreBreakdown
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)