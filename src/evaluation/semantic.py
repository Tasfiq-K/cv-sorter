from __future__ import annotations

from sentence_transformers import SentenceTransformer, util

from src.models import CandidateProfile, JobDescription


class SemanticScorer:
    """
    Calculate semantic relevance between a candidate profile
    and a job description using sentence embeddings.
    """

    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    DEFAULT_WEIGHTS = {
        "profile": 0.15,
        "experience": 0.20,
        "projects": 0.40,
        "context": 0.25
    }


    def __init__(
            self, 
            model_name: str = DEFAULT_MODEL,
            weights: dict[str, float] | None = None
    ):

        self.model = SentenceTransformer(model_name, device='cpu')
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

    
    def score(
        self, 
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        """
        Calculates the semantic match score between a candidate profile and a job description.
        Args:
            candidate: Pydantic model of the candidate profile. See `models.py` for  more info
            job_description: Pydantic model of the job description. See `models.py` for more info
        Returns:
             semantic score in the range of [0, 1]
        """

        components = {
            "profile": self._score_pair(
                self._build_candidate_profile(candidate),
                self._build_job_profile(job_description)
            ),

            "experience": self._score_pair(
                self._build_candidate_experience(candidate),
                self._build_job_experience(job_description)
            ),

            "projects": self._score_pair(
                self._build_candidate_projects(candidate),
                self._build_job_projects(job_description)
            ),

            "context": self._score_pair(
                self._build_candidate_context(candidate),
                self._build_job_context(job_description)
            ),
        }

        candidate_text = self._build_candidate(candidate)
        job_text = self._build_job(job_description)

        if not candidate_text or not job_text:
            return 0.0

        candidate_embedding = self.model.encode(
            candidate_text,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        job_embedding = self.model.encode(
            job_text,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        similarity = util.cos_sim(
            candidate_embedding,
            job_embedding
        ).item()

        return max(0.0, min(1.0, (similarity + 1.0) / 2.0))


    @staticmethod
    def _build_candidate(
        candidate: CandidateProfile,
    ) -> str:

        parts: list[str] = []

        if candidate.headline:
            parts.append(candidate.headline)

        if candidate.summary:
            parts.append(candidate.summary)

        for skill in candidate.skills:
            if skill.name:
                parts.append(skill.name)

        for experience in candidate.experience:
            if experience.role:
                parts.append(experience.role)

            if experience.description:
                parts.append(experience.description)

            if experience.technologies:
                parts.extend(experience.technologies)

        for project in candidate.projects:
            if project.title:
                parts.append(project.title)

            if project.description:
                parts.append(project.description)

            if project.technologies:
                parts.extend(project.technologies)

        return " ".join(parts).strip()


    @staticmethod
    def _build_job(
        job_description: JobDescription,
    ) -> str:

        parts: list[str] = []

        if job_description.title:
            parts.append(job_description.title)

        if job_description.summary:
            parts.append(job_description.summary)

        parts.extend(job_description.responsibilities)

        for skill in job_description.required_skills:
            if skill.name:
                parts.append(skill.name)

        for skill in job_description.preferred_skills:
            if skill.name:
                parts.append(skill.name)

        return " ".join(parts).strip()