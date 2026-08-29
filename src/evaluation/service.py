from __future__ import annotations

from src.models import (
    CandidateProfile,
    JobDescription,
    ScoreBreakdown,
)

from src.evaluation.evaluator import Evaluator
from src.evaluation.positions import get_position_profile


def evaluate_candidate(
    candidate: CandidateProfile,
    job_description: JobDescription,
    position: str,
) -> ScoreBreakdown:
    """
    Evaluate a candidate for a specific position.
    """

    position_profile = get_position_profile(position)

    evaluator = Evaluator(position_profile)

    return evaluator.evaluate(
        candidate=candidate,
        job_description=job_description,
    )