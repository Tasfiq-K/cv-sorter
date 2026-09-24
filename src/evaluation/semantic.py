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

        return self._weighted_average(components) # calculation happens elsewhere
    

    def _score_pair(
            self,
            candidate_text: str,
            job_text: str,
    ) -> float | None:

        """
        Calculate Cosine Similarity between texts.

        Args: 
            candidate_text: Textual information from candidate.
            job_text: Textual information from job description.

        Returns: 
            Similarity score between [0, 1]
        """

        if not candidate_text or not job_text:
            return None


        embeddings = self.model_encode(
            [candidate_text, job_text],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        # measure similarity

        similarity = util.cos_sim(
            embeddings[0],
            embeddings[1]
        ).item()

        return (0.0, min(1.0, similarity))


    def _weighted_average(
            self,
            components: dict[str, float | None],
    ) -> float:

        """
        Calculate a weighted average using only the available components.

        Args:
            components: A dict object containing the components as keys scores as values

        Retursn:
            Calculated weighted average.
        """

        weighted_sum = 0.0
        active_weight = 0.0

        for name, score in components.items():
            if score is None:
                continue

            default_weight = self.weights(name)

            weighted_sum += default_weight * score
            active_weight += default_weight

        if active_weight == 0.0:
            return 0.0

        return max(
            0.0,
            min(1.0, weighted_sum / active_weight)
        )

    # build candidate profile

    @staticmethod
    def _build_candidate_profile(
        candidate: CandidateProfile,
    ) -> str:

        parts: list[str] = []

        if candidate.headline:
            parts.append(candidate.headline)

        if candidate.summary:
            parts.append(candidate.summary)


        return " ".join(parts).strip()


    # build job profile
    @staticmethod
    def _build_job_profile(
        job_description: JobDescription,
    ) -> str:

        parts: list[str] = []

        if job_description.title:
            parts.append(job_description.title)

        if job_description.summary:
            parts.append(job_description.summary)

        return " ".join(parts).strip()


    # build candidate experience
    @staticmethod
    def _build_candidate_experience(
        candidate: CandidateProfile,
    ) -> str:

        parts: list[str] = []

        for experience in candidate.experience:
            if experience.role:
                parts.append(experience.role)

            if experience.description:
                parts.append(experience.description)

            if experience.technologies:
                parts.append(experience.technologies)

        return " ".join(parts).strip()


    # build experience needed for the job
    @staticmethod
    def _build_job_experience(
        job_description: JobDescription,
    ) -> str:

        parts: list[str] = []

        # get the experience needed for the job
        if job_description.experience:
            parts.append(job_description.experience)

        if job_description.summary:
            parts.append(job_description.summary)

        return " ".join(parts).strip()
        

    @staticmethod
    def _build_candidate_projects(
        candidate: CandidateProfile,
    ) -> str:

        parts: list[str] = []

        for project in candidate.projects:
            if project.title:
                parts.append(project.title)

            if project.description:
                parts.append(project.description)

            if project.technologies:
                parts.append(project.technologies)

        return " ".join(parts).strip()


    @staticmethod
    def _build_job_projects(
        job_description: JobDescription,
    ) -> str:

        parts: list[str] = []

        if job_description.summary:
            parts.append(job_description.summary)

        parts.extend(
            responsibility
            for responsibility in job_description.responsibilities
            if responsibility
        )

        return " ".join(parts).strip()