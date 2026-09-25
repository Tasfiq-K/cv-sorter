from __future__ import annotations

from src.models import EvaluationDimension, PositionProfile


# ==========================================================
# Machine Learning Intern
# ==========================================================

MACHINE_LEARNING_INTERN = PositionProfile(
    name="machine_learning_intern",
    description=(
        "Evaluation profile for entry-level machine learning "
        "internship candidates. Prioritizes technical foundation, "
        "relevant projects, learning potential, and education over "
        "professional experience."
    ),
    semantic_weight=0.10,
    evaluation_dimensions=[
        EvaluationDimension(
            name="required_skills",
            weight=0.25,
            description=(
                "Match against the technical skills explicitly "
                "required by the job description."
            ),
        ),
        EvaluationDimension(
            name="projects",
            weight=0.25,
            description=(
                "Relevant machine learning, deep learning, NLP, "
                "computer vision, data science, or similar projects."
            ),
        ),
        EvaluationDimension(
            name="learning_potential",
            weight=0.15,
            description=(
                "Evidence of curiosity, continuous learning, "
                "self-development, experimentation, and growth."
            ),
        ),
        EvaluationDimension(
            name="education",
            weight=0.10,
            description=(
                "Relevance of the candidate's educational background "
                "to the position."
            ),
        ),
        EvaluationDimension(
            name="communication_teamwork",
            weight=0.10,
            description=(
                "Evidence of communication, collaboration, teamwork, "
                "leadership, or related interpersonal abilities."
            ),
        ),
        EvaluationDimension(
            name="experience",
            weight=0.05,
            description=(
                "Relevant professional or internship experience. "
                "Experience is intentionally given a low weight because "
                "the position is suitable for freshers."
            ),
        ),
        EvaluationDimension(
            name="certifications",
            weight=0.05,
            description=(
                "Relevant certifications, courses, or structured "
                "technical learning."
            ),
        ),
        EvaluationDimension(
            name="technical_depth",
            weight=0.05,
            description=(
                "Depth and breadth of the candidate's technical "
                "knowledge beyond the explicitly required skills."
            ),
        ),
    ],
)


# ==========================================================
# Machine Learning Engineer
# ==========================================================

MACHINE_LEARNING_ENGINEER = PositionProfile(
    name="machine_learning_engineer",
    description=(
        "Evaluation profile for machine learning engineering roles. "
        "Prioritizes professional experience, technical skills, "
        "projects, and technical depth."
    ),
    semantic_weight=0.10,
    evaluation_dimensions=[
        EvaluationDimension(
            name="experience",
            weight=0.30,
            description="Relevant professional machine learning experience.",
        ),
        EvaluationDimension(
            name="required_skills",
            weight=0.25,
            description="Match against explicitly required technical skills.",
        ),
        EvaluationDimension(
            name="technical_depth",
            weight=0.15,
            description="Depth of machine learning and engineering knowledge.",
        ),
        EvaluationDimension(
            name="projects",
            weight=0.10,
            description="Relevant and technically substantial projects.",
        ),
        EvaluationDimension(
            name="education",
            weight=0.05,
            description="Relevance of academic background.",
        ),
        EvaluationDimension(
            name="certifications",
            weight=0.05,
            description="Relevant professional certifications and courses.",
        ),
        EvaluationDimension(
            name="communication_teamwork",
            weight=0.05,
            description="Communication and collaboration ability.",
        ),
        EvaluationDimension(
            name="learning_potential",
            weight=0.05,
            description="Evidence of continued technical growth.",
        ),
    ],
)


# ==========================================================
# Data Scientist
# ==========================================================

DATA_SCIENTIST = PositionProfile(
    name="data_scientist",
    description=(
        "Evaluation profile for data science roles. Prioritizes "
        "relevant experience, analytical and machine learning skills, "
        "projects, and technical depth."
    ),
    semantic_weight=0.10,
    evaluation_dimensions=[
        EvaluationDimension(
            name="required_skills",
            weight=0.25,
            description="Match against required data science skills.",
        ),
        EvaluationDimension(
            name="experience",
            weight=0.25,
            description="Relevant data science and analytical experience.",
        ),
        EvaluationDimension(
            name="technical_depth",
            weight=0.15,
            description="Depth in statistics, machine learning, and data analysis.",
        ),
        EvaluationDimension(
            name="projects",
            weight=0.15,
            description="Relevant data science and machine learning projects.",
        ),
        EvaluationDimension(
            name="education",
            weight=0.10,
            description="Relevant academic background.",
        ),
        EvaluationDimension(
            name="communication_teamwork",
            weight=0.05,
            description="Communication and collaboration ability.",
        ),
        EvaluationDimension(
            name="certifications",
            weight=0.05,
            description="Relevant certifications and technical courses.",
        ),
    ],
)


# ==========================================================
# Software Engineer
# ==========================================================

SOFTWARE_ENGINEER = PositionProfile(
    name="software_engineer",
    description=(
        "Evaluation profile for software engineering roles. "
        "Prioritizes software development experience, required "
        "technical skills, projects, and engineering depth."
    ),
    semantic_weight=0.10,
    evaluation_dimensions=[
        EvaluationDimension(
            name="required_skills",
            weight=0.30,
            description="Match against required programming and engineering skills.",
        ),
        EvaluationDimension(
            name="experience",
            weight=0.25,
            description="Relevant professional software engineering experience.",
        ),
        EvaluationDimension(
            name="technical_depth",
            weight=0.15,
            description="Depth of software engineering knowledge.",
        ),
        EvaluationDimension(
            name="projects",
            weight=0.15,
            description="Relevant software engineering projects.",
        ),
        EvaluationDimension(
            name="education",
            weight=0.05,
            description="Relevant educational background.",
        ),
        EvaluationDimension(
            name="communication_teamwork",
            weight=0.05,
            description="Communication and collaboration ability.",
        ),
        EvaluationDimension(
            name="certifications",
            weight=0.05,
            description="Relevant certifications and courses.",
        ),
    ],
)


# ==========================================================
# Position Registry
# ==========================================================

POSITION_PROFILES: dict[str, PositionProfile] = {
    MACHINE_LEARNING_INTERN.name: MACHINE_LEARNING_INTERN,
    MACHINE_LEARNING_ENGINEER.name: MACHINE_LEARNING_ENGINEER,
    DATA_SCIENTIST.name: DATA_SCIENTIST,
    SOFTWARE_ENGINEER.name: SOFTWARE_ENGINEER,
}


def get_position_profile(position: str) -> PositionProfile:
    """
    Return the evaluation profile for a position.

    Parameters
    ----------
    position:
        Position identifier, e.g. "machine_learning_intern".

    Raises
    ------
    ValueError
        If no profile exists for the requested position.
    """

    try:
        return POSITION_PROFILES[position]
    except KeyError:
        available = ", ".join(sorted(POSITION_PROFILES))

        raise ValueError(
            f"Unknown position '{position}'. "
            f"Available positions: {available}"
        )

if __name__ == "__main__":


    pp = get_position_profile("machine_learning_intern")
    print(pp)