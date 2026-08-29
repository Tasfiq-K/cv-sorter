from __future__ import annotations

from src.evaluation.evaluator import Evaluator
from src.evaluation.positions import get_position_profile
from src.models import (
    CandidateProfile,
    CertificationEntry,
    ContactInfo,
    EducationEntry,
    ExperienceEntry,
    ProjectEntry,
    SkillEntry,
)


def make_candidate() -> CandidateProfile:
    """
    Create a deterministic candidate profile for evaluator tests.
    """

    return CandidateProfile(
        name="Test Candidate",
        headline="Machine Learning Engineer",
        summary="Machine learning candidate with relevant projects and experience.",
        contact=ContactInfo(
            email="test@example.com",
            phone=None,
            location="Dhaka",
            linkedin=None,
            github=None,
            portfolio=None,
        ),
        skills=[
            SkillEntry(
                name="Python",
                category="Programming Language",
            ),
            SkillEntry(
                name="PyTorch",
                category="Machine Learning Framework",
            ),
            SkillEntry(
                name="Scikit-learn",
                category="Machine Learning",
            ),
        ],
        education=[
            EducationEntry(
                institution="Test University",
                degree="BSc",
                field_of_study="Computer Science",
                grade="CGPA 3.50/4.00",
                start_date_raw="2019",
                end_date_raw="2023",
                description=None,
            )
        ],
        experience=[
            ExperienceEntry(
                company="Test Company",
                role="Machine Learning Engineer",
                employment_type="Full-time",
                location="Dhaka",
                start_date_raw="2023",
                end_date_raw="Present",
                currently_working=True,
                technologies=["Python", "PyTorch"],
                description="Developed machine learning models.",
            )
        ],
        projects=[
            ProjectEntry(
                title="ML Project",
                description="Machine learning classification project.",
                technologies=["Python", "Scikit-learn"],
                github=None,
                demo=None,
            )
        ],
        certifications=[
            CertificationEntry(
                name="Machine Learning Certificate",
                issuer="Test Institute",
                issue_date_raw="2023",
            )
        ],
        languages=[],
        raw_text="Test candidate raw text.",
    )


def make_job_description():
    """
    Create a minimal deterministic job description.

    This should match the fields currently consumed by Evaluator.
    """

    from src.models import (
        ExperienceRequirement,
        JobDescription,
    )

    return JobDescription(
        title="Machine Learning Intern",
        company="Test Company",
        location="Dhaka",
        employment_type="On-site",
        seniority="Intern",
        summary="Machine learning internship.",
        responsibilities=[
            "Develop machine learning models.",
        ],
        required_skills=[
            SkillEntry(
                name="Python",
                category="Programming Language",
            ),
            SkillEntry(
                name="TensorFlow",
                category="Machine Learning Framework",
            ),
        ],
        preferred_skills=[
            SkillEntry(
                name="PyTorch",
                category="Machine Learning Framework",
            ),
        ],
        experience=ExperienceRequirement(
            minimum_years=0.0,
            maximum_years=None,
            raw_requirement="Freshers",
            required=True,
        ),
        education=[],
        certifications=[],
        other_requirements=[],
        raw_text="Test job description.",
    )


def make_evaluator() -> Evaluator:
    position = get_position_profile("machine_learning_intern")

    return Evaluator(position)


# ==========================================================
# Position / Weight Tests
# ==========================================================


def test_position_profile_loads():
    position = get_position_profile("machine_learning_intern")

    assert position.name == "machine_learning_intern"
    assert position.evaluation_dimensions


def test_position_weights_are_loaded():
    evaluator = make_evaluator()

    assert evaluator._weights["required_skills"] == 0.25
    assert evaluator._weights["projects"] == 0.25
    assert evaluator._weights["education"] == 0.10
    assert evaluator._weights["experience"] == 0.05
    assert evaluator._weights["certifications"] == 0.05


# ==========================================================
# Skill Tests
# ==========================================================


def test_required_skill_score():
    evaluator = make_evaluator()
    job = make_job_description()

    matched_skills = ["Python"]

    score = evaluator._required_skill_score(
        matched_skills,
        job,
    )

    assert score == 0.5


def test_preferred_skill_score():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    score = evaluator._preferred_skill_score(
        candidate,
        job,
    )

    # Candidate has PyTorch, which is the only preferred skill.
    assert score == 1.0


# ==========================================================
# Experience Tests
# ==========================================================


def test_experience_score_when_requirement_is_met():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    score = evaluator._experience_score(
        candidate,
        job,
    )

    assert score == 1.0


# ==========================================================
# Education Tests
# ==========================================================


def test_education_score_when_no_requirement_exists():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    score = evaluator._education_score(
        candidate,
        job,
    )

    assert score == 1.0


# ==========================================================
# Project Tests
# ==========================================================


def test_project_score_when_candidate_has_projects():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    score = evaluator._project_score(
        candidate,
        job,
    )

    assert score == 1.0


# ==========================================================
# Certification Tests
# ==========================================================


def test_certification_score_when_no_requirement_exists():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    score = evaluator._certification_score(
        candidate,
        job,
    )

    assert score == 1.0


# ==========================================================
# Final Score Tests
# ==========================================================


def test_final_score_is_weighted_sum():
    evaluator = make_evaluator()

    score = evaluator._build_score_breakdown(
        required_skill_score=0.5,
        preferred_skill_score=1.0,
        experience_score=1.0,
        education_score=1.0,
        project_score=1.0,
        certification_score=1.0,
    )

    expected = (
        0.5 * 0.25
        # + 1.0 * 0.25
        + 1.0 * 0.05
        + 1.0 * 0.10
        + 1.0 * 0.25
        + 1.0 * 0.05
    )

    print(f"final score: {score.final_score}\nexpected: {expected}\n")
    assert score.final_score == expected


# ==========================================================
# Full Evaluation Test
# ==========================================================


def test_evaluate_returns_complete_result():
    evaluator = make_evaluator()

    candidate = make_candidate()
    job = make_job_description()

    result = evaluator.evaluate(
        candidate=candidate,
        job_description=job,
    )

    assert result.profile == candidate

    assert result.features is not None
    assert result.score is not None

    assert result.score.required_skill_score == 0.5
    assert result.score.preferred_skill_score == 1.0

    assert result.score.experience_score == 1.0
    assert result.score.education_score == 1.0
    assert result.score.project_score == 1.0
    assert result.score.certification_score == 1.0

    assert result.score.final_score > 0.0

    assert isinstance(result.matched_skills, list)
    assert isinstance(result.missing_skills, list)
    assert isinstance(result.strengths, list)


# ==========================================================
# Negative / Edge Cases
# ==========================================================


def test_candidate_with_no_skills():
    evaluator = make_evaluator()

    candidate = make_candidate()
    candidate.skills = []

    job = make_job_description()

    matched_skills = []

    score = evaluator._required_skill_score(
        matched_skills,
        job,
    )
    # print(f"No skills score: {score}")
    assert score == 0.0


def test_candidate_with_no_projects():
    evaluator = make_evaluator()

    candidate = make_candidate()
    candidate.projects = []

    job = make_job_description()

    score = evaluator._project_score(
        candidate,
        job,
    )

    assert score == 0.0


def test_unknown_position_raises_error():
    try:
        get_position_profile("unknown_position")
    except ValueError as exc:
        assert "Unknown position" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for unknown position"
        )


if __name__ == "__main__":
    test_position_profile_loads()
    test_position_weights_are_loaded()

    test_required_skill_score()
    test_preferred_skill_score()

    test_experience_score_when_requirement_is_met()
    test_education_score_when_no_requirement_exists()
    test_project_score_when_candidate_has_projects()
    test_certification_score_when_no_requirement_exists()

    test_final_score_is_weighted_sum()
    test_evaluate_returns_complete_result()

    test_candidate_with_no_skills()
    test_candidate_with_no_projects()

    test_unknown_position_raises_error()

    print("All evaluator tests passed.")
