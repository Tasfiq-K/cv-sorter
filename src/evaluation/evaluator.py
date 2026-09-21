from __future__ import annotations

from datetime import date
import re

from src.models import (
    CandidateProfile,
    JobDescription,
    PositionProfile,
    CandidateFeatures,
    ScoreBreakdown,
    RankedCandidate,
)
from .semantic import SemanticScorer

class Evaluator:
    """
    Deterministic candidate evaluator.

    The evaluator combines:
        - CandidateProfile
        - JobDescription
        - PositionProfile

    and produces a RankedCandidate.

    No LLM calls are performed here.
    """

    def __init__(self, position: PositionProfile):
        self.position = position

        self._weights = {
            dimension.name: dimension.weight
            for dimension in position.evaluation_dimensions
        }

        self.semantic_scorer = SemanticScorer()

    # ==========================================================
    # Public API
    # ==========================================================

    def evaluate(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> RankedCandidate:

        features = self._build_features(candidate)

        matched_skills, missing_skills = self._match_required_skills(
            candidate,
            job_description,
        )

        required_skill_score = self._required_skill_score(
            matched_skills,
            job_description,
        )

        preferred_skill_score = self._preferred_skill_score(
            candidate,
            job_description,
        )

        experience_score = self._experience_score(
            candidate,
            job_description,
        )

        education_score = self._education_score(
            candidate,
            job_description,
        )

        project_score = self._project_score(
            candidate,
            job_description,
        )

        certification_score = self._certification_score(
            candidate,
            job_description,
        )

        semantic_score = self.semantic_scorer.score(
            candidate,
            job_description,
        )

        # throw-away print statement
        print(f"Semantic Score: {semantic_score}")

        score = self._build_score_breakdown(
            required_skill_score=required_skill_score,
            preferred_skill_score=preferred_skill_score,
            experience_score=experience_score,
            education_score=education_score,
            project_score=project_score,
            certification_score=certification_score,
            semantic_score=semantic_score,
        )

        strengths = self._find_strengths(
            candidate=candidate,
            job_description=job_description,
            matched_skills=matched_skills,
            score=score,
        )

        return RankedCandidate(
            profile=candidate,
            features=features,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            strengths=strengths,
        )

    # ==========================================================
    # Candidate Features
    # ==========================================================

    def _build_features(
        self,
        candidate: CandidateProfile,
    ) -> CandidateFeatures:

        total_experience_months = self._calculate_experience_months(
            candidate
        )

        internship_count = sum(
            1
            for experience in candidate.experience
            if self._is_internship(experience.role)
        )

        highest_degree = self._highest_degree(candidate)

        normalized_skills = [
            self._normalize(skill.name)
            for skill in candidate.skills
        ]

        return CandidateFeatures(
            total_experience_months=total_experience_months,
            relevant_experience_months=0,
            internship_count=internship_count,
            project_count=len(candidate.projects),
            certification_count=len(candidate.certifications),
            highest_degree=highest_degree,
            normalized_skills=normalized_skills,
        )

    # ==========================================================
    # Skill Matching
    # ==========================================================

    def _match_required_skills(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> tuple[list[str], list[str]]:

        candidate_skills = {
            self._normalize(skill.name)
            for skill in candidate.skills
        }

        matched: list[str] = []
        missing: list[str] = []

        for requirement in job_description.required_skills:

            required = self._normalize(requirement.name)

            if self._skill_matches(required, candidate_skills):
                matched.append(requirement.name)
            else:
                missing.append(requirement.name)

        return matched, missing

    def _required_skill_score(
        self,
        matched_skills: list[str],
        job_description: JobDescription,
    ) -> float:

        total = len(job_description.required_skills)

        if total == 0:
            return 1.0

        return len(matched_skills) / total

    def _preferred_skill_score(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        if not job_description.preferred_skills:
            return 1.0

        candidate_skills = {
            self._normalize(skill.name)
            for skill in candidate.skills
        }

        matched = 0

        for skill in job_description.preferred_skills:
            if self._skill_matches(
                self._normalize(skill.name),
                candidate_skills,
            ):
                matched += 1

        return matched / len(job_description.preferred_skills)

    # ==========================================================
    # Experience
    # ==========================================================

    def _experience_score(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        requirement = job_description.experience

        # No experience requirement.
        if (
            requirement.minimum_years is None
            and requirement.maximum_years is None
        ):
            return 1.0

        candidate_years = (
            self._calculate_experience_months(candidate) / 12
        )

        minimum = requirement.minimum_years

        if minimum is None:
            return 1.0

        if minimum == 0:
            return 1.0

        return min(candidate_years / minimum, 1.0)

    # ==========================================================
    # Education
    # ==========================================================

    def _education_score(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        if not job_description.education:
            return 1.0

        if not candidate.education:
            return 0.0

        matched = 0

        for requirement in job_description.education:

            for education in candidate.education:

                degree_match = self._text_matches(
                    requirement.degree,
                    education.degree,
                )

                field_match = self._text_matches(
                    requirement.field_of_study,
                    education.field_of_study,
                )

                # If the requirement has a field, both degree/field
                # information should support the requirement.
                if requirement.field_of_study:
                    if field_match or self._text_matches(
                        requirement.field_of_study,
                        education.degree,
                    ):
                        matched += 1
                        break

                elif requirement.degree and degree_match:
                    matched += 1
                    break

                elif not requirement.degree and not requirement.field_of_study:
                    matched += 1
                    break

        return matched / len(job_description.education)

    # ==========================================================
    # Projects
    # ==========================================================

    def _project_score(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        if not candidate.projects:
            return 0.0

        # The first implementation intentionally uses skill overlap.
        #
        # Semantic project relevance will be added later.
        required_skills = {
            self._normalize(skill.name)
            for skill in job_description.required_skills
        }

        preferred_skills = {
            self._normalize(skill.name)
            for skill in job_description.preferred_skills
        }

        target_skills = required_skills | preferred_skills

        if not target_skills:
            return 1.0

        relevant_projects = 0

        for project in candidate.projects:

            project_skills = {
                self._normalize(skill)
                for skill in project.technologies
            }

            project_text = self._normalize(
                f"{project.title or ''} "
                f"{project.description or ''}"
            )

            if any(
                skill in project_skills
                or skill in project_text
                for skill in target_skills
            ):
                relevant_projects += 1

        return min(
            relevant_projects / len(candidate.projects),
            1.0,
        )

    # ==========================================================
    # Certifications
    # ==========================================================

    def _certification_score(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
    ) -> float:

        if not job_description.certifications:
            return 1.0

        if not candidate.certifications:
            return 0.0

        matched = 0

        candidate_certifications = [
            self._normalize(cert.name)
            for cert in candidate.certifications
            if cert.name
        ]

        for requirement in job_description.certifications:

            requirement_name = self._normalize(requirement.name)

            if any(
                requirement_name in certification
                or certification in requirement_name
                for certification in candidate_certifications
            ):
                matched += 1

        return matched / len(job_description.certifications)

    # ==========================================================
    # Final Score
    # ==========================================================

    def _build_score_breakdown(
        self,
        *,
        required_skill_score: float,
        preferred_skill_score: float,
        experience_score: float,
        education_score: float,
        project_score: float,
        certification_score: float,
        semantic_score: float,
    ) -> ScoreBreakdown:

        scores = {
            "required_skills": required_skill_score,
            "preferred_skills": preferred_skill_score,
            "experience": experience_score,
            "education": education_score,
            "projects": project_score,
            "certifications": certification_score,
        }

        weighted_total = 0.0

        for dimension, score in scores.items():
            weighted_total += (
                score * self._weights.get(dimension, 0.0)
            )

        # Dimensions not yet implemented:
        #
        # - technical_depth
        # - learning_potential
        # - communication_teamwork
        # - semantic relevance
        #
        # Their scores remain 0 until implemented.

        return ScoreBreakdown(
            required_skill_score=required_skill_score,
            preferred_skill_score=preferred_skill_score,
            experience_score=experience_score,
            education_score=education_score,
            project_score=project_score,
            certification_score=certification_score,
            semantic_score=semantic_score,
            final_score=weighted_total,
        )

    # ==========================================================
    # Strengths
    # ==========================================================

    def _find_strengths(
        self,
        *,
        candidate: CandidateProfile,
        job_description: JobDescription,
        matched_skills: list[str],
        score: ScoreBreakdown,
    ) -> list[str]:

        strengths: list[str] = []

        if matched_skills:
            strengths.append(
                f"Matches {len(matched_skills)} required skill(s)."
            )

        if candidate.projects:
            strengths.append(
                f"Has {len(candidate.projects)} project(s)."
            )

        if candidate.experience:
            strengths.append(
                f"Has {len(candidate.experience)} experience entry/entries."
            )

        if score.experience_score >= 1.0:
            strengths.append(
                "Meets the stated experience requirement."
            )

        if score.project_score >= 0.5:
            strengths.append(
                "Has projects with relevant technical overlap."
            )

        if score.education_score >= 1.0:
            strengths.append(
                "Meets the stated education requirements."
            )

        return strengths

    # ==========================================================
    # Experience Helpers
    # ==========================================================

    def _calculate_experience_months(
        self,
        candidate: CandidateProfile,
    ) -> int:

        total_months = 0

        for experience in candidate.experience:

            start = self._parse_date(experience.start_date_raw)

            if start is None:
                continue

            if experience.currently_working:
                end = date.today()
            else:
                end = self._parse_date(experience.end_date_raw)

            if end is None:
                continue

            months = (
                (end.year - start.year) * 12
                + (end.month - start.month)
            )

            if months > 0:
                total_months += months

        return total_months

    @staticmethod
    def _parse_date(value: str | None) -> date | None:
        """
        Parse the common date formats produced by the CV parser.

        This intentionally handles only simple formats for now.
        More robust date normalization can be added later.
        """

        if not value:
            return None

        value = value.strip()

        patterns = [
            (r"^([A-Za-z]+)\s+(\d{4})$", "%B %Y"),
            (r"^([A-Za-z]+)(\d{4})$", "%B%Y"),
            (r"^(\d{4})$", "%Y"),
        ]

        for pattern, date_format in patterns:

            if not re.match(pattern, value):
                continue

            try:
                from datetime import datetime

                return datetime.strptime(
                    value,
                    date_format,
                ).date()

            except ValueError:
                # Try abbreviated month names.
                try:
                    if "%B" in date_format:
                        return datetime.strptime(
                            value,
                            date_format.replace("%B", "%b"),
                        ).date()
                except ValueError:
                    pass

        return None

    @staticmethod
    def _is_internship(role: str | None) -> bool:

        if not role:
            return False

        return "intern" in role.lower()

    # ==========================================================
    # Education Helpers
    # ==========================================================

    @staticmethod
    def _highest_degree(
        candidate: CandidateProfile,
    ) -> str | None:

        if not candidate.education:
            return None

        degree_order = {
            "phd": 4,
            "doctorate": 4,
            "master": 3,
            "msc": 3,
            "mba": 3,
            "bachelor": 2,
            "bsc": 2,
            "bsc engineering": 2,
            "undergraduate": 2,
            "diploma": 1,
        }

        best_degree = None
        best_rank = -1

        for education in candidate.education:

            if not education.degree:
                continue

            degree = Evaluator._normalize(education.degree)

            for name, rank in degree_order.items():

                if name in degree and rank > best_rank:
                    best_degree = education.degree
                    best_rank = rank

        return best_degree

    # ==========================================================
    # Text / Skill Helpers
    # ==========================================================

    @staticmethod
    def _normalize(value: str) -> str:

        value = value.lower().strip()

        value = re.sub(r"[^a-z0-9+#.]+", " ", value)

        return re.sub(r"\s+", " ", value)

    def _skill_matches(
        self,
        required_skill: str,
        candidate_skills: set[str],
    ) -> bool:

        if required_skill in candidate_skills:
            return True

        for candidate_skill in candidate_skills:

            if (
                required_skill in candidate_skill
                or candidate_skill in required_skill
            ):
                return True

        return False

    def _text_matches(
        self,
        required: str | None,
        candidate: str | None,
    ) -> bool:

        if not required or not candidate:
            return False

        required = self._normalize(required)
        candidate = self._normalize(candidate)

        return (
            required in candidate
            or candidate in required
        )