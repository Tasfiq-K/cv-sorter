from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


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
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

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

    model_config = ConfigDict(extra="forbid")

    title: str | None 
    description: str | None 
    technologies: list[str] 
    github: str | None 
    demo: str | None 


# ============================================================================
# Certifications
# ============================================================================


class CertificationEntry(BaseModel):

    model_config = ConfigDict(extra="forbid")

    name: str | None 
    issuer: str | None 
    issue_date_raw: str | None 


# ============================================================================
# Skills
# ============================================================================


class SkillEntry(BaseModel):

    model_config = ConfigDict(extra="forbid")

    name: str
    category: str | None 


# ============================================================================
# Languages
# ============================================================================


class LanguageEntry(BaseModel):

    model_config = ConfigDict(extra="forbid")

    name: str
    proficiency: str | None 


class RequirementEntry(BaseModel):
    """
    A requirement extracted from a job description.

    priority:
        How important the requirement appears to be.

    required:
        Whether the requirement is explicitly required or merely preferred.
    """

    model_config = ConfigDict(extra="forbid")

    name: str
    required: bool
    priority: str | None
    description: str | None


class ExperienceRequirement(BaseModel):
    """
    Experience requirement extracted from a job description.

    Values remain close to the original wording.
    """

    model_config = ConfigDict(extra="forbid")

    minimum_years: float | None
    maximum_years: float | None
    raw_requirement: str | None
    required: bool


class EducationRequirement(BaseModel):
    """
    Educational qualification required or preferred by the employer.
    """

    model_config = ConfigDict(extra="forbid")

    degree: str | None
    field_of_study: str | None
    required: bool
    description: str | None

# ============================================================================
# Parsed Resume
# ============================================================================


class CandidateProfile(BaseModel):
    """
    Complete parsed candidate profile used internally by the application.
    """

    model_config = ConfigDict(extra="forbid")

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


class CandidateProfileLLM(BaseModel):
    """
    Structured information extracted directly by the LLM.

    This model is used exclusively as the Groq structured-output schema.
    """

    model_config = ConfigDict(extra="forbid")

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

# ============================================================================
# Parsed Job Description
# ============================================================================


class JobDescription(BaseModel):
    """
    Complete structured job description used by the application.

    raw_text is preserved from the original document and is not
    generated by the LLM.
    """

    model_config = ConfigDict(extra="forbid")

    title: str | None
    company: str | None
    location: str | None
    employment_type: str | None
    seniority: str | None

    summary: str | None

    responsibilities: list[str]

    required_skills: list[SkillEntry]
    preferred_skills: list[SkillEntry]

    experience: ExperienceRequirement

    education: list[EducationRequirement]

    certifications: list[RequirementEntry]

    other_requirements: list[RequirementEntry]

    raw_text: str



class JobDescriptionLLM(BaseModel):
    """
    Structured job description returned directly by the LLM.

    This model is used as the Groq structured-output schema.
    """

    model_config = ConfigDict(extra="forbid")

    title: str | None
    company: str | None
    location: str | None
    employment_type: str | None
    seniority: str | None

    summary: str | None

    responsibilities: list[str]

    required_skills: list[SkillEntry]
    preferred_skills: list[SkillEntry]

    experience: ExperienceRequirement

    education: list[EducationRequirement]

    certifications: list[RequirementEntry]

    other_requirements: list[RequirementEntry]

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

# ==========================================================
# Position / Evaluation Models
# ==========================================================

class EvaluationDimension(BaseModel):
    """
    A dimension used when evaluating a candidate for a
    particular position.

    This is application-level evaluation strategy.
    It is NOT extracted from the job description.
    """

    model_config = ConfigDict(extra="forbid")

    name: str

    weight: float = Field(
        ge=0.0,
        le=1.0
    )

    description: str | None


class PositionProfile(BaseModel):
    """
    Defines how candidates should be evaluated for a
    particular type of position.

    Examples:
        machine_learning_intern
        machine_learning_engineer
        data_scientist
        software_engineer
    """

    model_config = ConfigDict(extra="forbid")

    name: str

    description: str

    semantic_weight: float = Field(ge=0.0, le=1.0)

    evaluation_dimensions: list[EvaluationDimension] = Field(
        default_factory=list
    )


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
    explicit_score: float = 0.0
    final_score: float = 0.0


class RankedCandidate(BaseModel):

    profile: CandidateProfile
    features: CandidateFeatures
    score: ScoreBreakdown
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]