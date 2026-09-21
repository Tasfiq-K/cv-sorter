from __future__ import annotations

from src.evaluation.semantic import SemanticScorer
from src.models import (
    CandidateProfile,
    ContactInfo,
    JobDescription,
    ExperienceRequirement,
)

scorer = SemanticScorer()

def make_candidate(
    *,
    skills: list[str],
    summary: str | None = None,
    headline: str | None = "Machine Learning Engineer",
) -> CandidateProfile:

    return CandidateProfile(
        name="Test Candidate",
        headline=headline,
        summary=summary,
        contact=ContactInfo(
            email=None,
            phone=None,
            location=None,
            linkedin=None,
            github=None,
            portfolio=None,
        ),
        skills=[
            {
                "name": skill,
                "category": None,
            }
            for skill in skills
        ],
        education=[],
        experience=[],
        projects=[],
        certifications=[],
        languages=[],
        raw_text="",
    )


def make_job(
    *,
    title: str,
    summary: str,
    responsibilities: list[str],
    required_skills: list[str],
) -> JobDescription:

    return JobDescription(
        title=title,
        company="Test Company",
        location=None,
        employment_type=None,
        seniority=None,
        summary=summary,
        responsibilities=responsibilities,
        required_skills=[
            {
                "name": skill,
                "category": None,
            }
            for skill in required_skills
        ],
        preferred_skills=[],
        experience=ExperienceRequirement(
            minimum_years=None,
            maximum_years=None,
            raw_requirement=None,
            required=False,
        ),
        education=[],
        certifications=[],
        other_requirements=[],
        raw_text="",
    )


def test_related_candidate_scores_higher():

    # scorer = SemanticScorer()

    candidate = make_candidate(
        skills=[
            "Python",
            "Machine Learning",
            "PyTorch",
            "Computer Vision",
        ],
        summary=(
            "Machine learning engineer developing computer vision "
            "models using Python and PyTorch."
        ),
    )

    job = make_job(
        title="Machine Learning Intern",
        summary=(
            "Work on machine learning and computer vision "
            "applications."
        ),
        responsibilities=[
            "Develop and test machine learning models.",
        ],
        required_skills=[
            "Python",
            "Machine Learning",
        ],
    )

    score = scorer.score(candidate, job)

    print(f"[Related candidate] semantic score: {score}")

    assert 0.0 <= score <= 1.0


def test_unrelated_candidate_can_be_scored():

    # scorer = SemanticScorer()

    candidate = make_candidate(
        skills=[
            "Accounting",
            "Taxation",
            "Financial Reporting",
        ],
        summary=(
            "Accounting professional specializing in financial "
            "reporting and taxation."
        ),
    )

    job = make_job(
        title="Machine Learning Intern",
        summary=(
            "Work on machine learning and computer vision "
            "applications."
        ),
        responsibilities=[
            "Develop and test machine learning models.",
        ],
        required_skills=[
            "Python",
            "Machine Learning",
        ],
    )

    score = scorer.score(candidate, job)

    print(f"[Unrelated candidate] semantic score: {score}")

    assert 0.0 <= score <= 1.0


def test_empty_candidate_returns_zero():

    # scorer = SemanticScorer()

    candidate = make_candidate(
        skills=[],
        summary=None,
        headline=None,
    )

    job = make_job(
        title="Machine Learning Intern",
        summary="Machine learning internship.",
        responsibilities=[
            "Develop machine learning models.",
        ],
        required_skills=[
            "Python",
        ],
    )

    score = scorer.score(candidate, job)
    print(f"[Empty cnadidate] semantic score: {score}")

    assert score == 0.0


if __name__ == "__main__":
    print("Starting...")
    test_related_candidate_scores_higher()
    test_unrelated_candidate_can_be_scored()
    test_empty_candidate_returns_zero()

    print("All semantic scorer tests passed.")