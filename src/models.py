from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# Document Models
# ==========================================================


class Document(BaseModel):
    """
    Base class for all extracted documents    
    """

    filename: str
    path: Path
    extension: str

    raw_text: str

    page_count: int | None 
    character_count: int


class CandidateDocument(Document):
    """
    Raw resume extracted from a file.
    """
    pass


class JobDescriptionDocument(Document):
    """
    Raw job description extracted from a file.
    """
    pass


# ============================================================================
# Contact Information
# ============================================================================


class ContactInfo(BaseModel):

    email: str | None 
    phone: str | None 
    location: str | None 
    linkedin: str | None 
    github: str | None 
    portfolio: str | None 


# ============================================================================
# Education
# ============================================================================


class EducationEntry(BaseModel):
    """
    Exactly as extracted by the LLM.

    No normalization happens here.
    """

    institution: str | None 
    degree: str | None 
    field_of_study: str | None 
    grade: str | None 
    start_date_raw: str | None 
    end_date_raw: str | None 
    description: str | None 


# ============================================================================
# Experience
# ============================================================================


class ExperienceEntry(BaseModel):
    """
    Raw employment history.

    Dates remain exactly as written in the CV.
    """

    company: str | None 
    role: str | None 
    employment_type: str | None 
    location: str | None 
    start_date_raw: str | None 
    end_date_raw: str | None 
    currently_working: bool | None 
    technologies: list[str] 
    description: str | None 


# ============================================================================
# Projects
# ============================================================================


class ProjectEntry(BaseModel):

    title: str | None 
    description: str | None 
    technologies: list[str] 
    github: str | None 
    demo: str | None 


# ============================================================================
# Certifications
# ============================================================================


class CertificationEntry(BaseModel):

    name: str | None 
    issuer: str | None 
    issue_date_raw: str | None 


# ============================================================================
# Skills
# ============================================================================


class SkillEntry(BaseModel):

    name: str
    category: str | None 


# ============================================================================
# Languages
# ============================================================================


class LanguageEntry(BaseModel):

    name: str
    proficiency: str | None 


# ============================================================================
# Parsed Resume
# ============================================================================


class CandidateProfile(BaseModel):
    """
    Structured resume returned by the LLM.

    This model intentionally stores extracted facts only.
    No derived information belongs here.
    """

    name: str | None 
    headline: str | None 
    summary: str | None 
    contact: ContactInfo 
    skills: list[SkillEntry] 
    education: list[EducationEntry]  
    experience: list[ExperienceEntry]
    projects: list[ProjectEntry] 
    certifications: list[CertificationEntry] 
    languages: list[LanguageEntry]
    raw_text: str


# ============================================================================
# Parsed Job Description
# ============================================================================


class JobDescription(BaseModel):
    """
    Structured Job Description returned by the LLM.
    """

    title: str | None 
    company: str | None 
    location: str | None 
    employment_type: str | None 
    summary: str | None 
    responsibilities: list[str] 
    required_skills: list[str] 
    preferred_skills: list[str] 
    required_education: list[str] 
    preferred_education: list[str] 
    required_certifications: list[str] 
    preferred_certifications: list[str] 
    experience_requirement: str | None 
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
    highest_degree: str | None 
    normalized_skills: list[str] 


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
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]