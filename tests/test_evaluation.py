from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv

from src.extractor import extract_text
from src.parser import Parser
from src.llm.groq import GroqLLM
from src.evaluation.positions import get_position_profile
from src.evaluation.service import evaluate_candidate

load_dotenv()
POSITION = 'machine_learning_intern'

def main():

    jd_path = Path("data/job_descriptions/jd.md")
    cv_path = Path("data/cvs/Md Tasfiq Kamran.pdf")

    # --------------------------------------------------
    # Initialize LLM / parser
    # --------------------------------------------------

    llm = GroqLLM()
    parser = Parser(llm)

    # --------------------------------------------------
    # Parse Job Description
    # --------------------------------------------------

    print("Parsing job description...")

    jd_document = extract_text(jd_path)

    job_description = parser.parse_jd(jd_document)

    print("\n" + "=" * 70)
    print("JOB DESCRIPTION")
    print("=" * 70)

    pprint(job_description.model_dump())

    # --------------------------------------------------
    # Parse Candidate
    # --------------------------------------------------

    print("\nParsing candidate CV...")

    cv_document = extract_text(cv_path)

    candidate = parser.parse_resume(cv_document)

    print("\n" + "=" * 70)
    print("CANDIDATE")
    print("=" * 70)

    pprint(candidate.model_dump())

    # --------------------------------------------------
    # Position
    # --------------------------------------------------

    # position = get_position_profile(
    #     "machine_learning_intern"
    # )

    # --------------------------------------------------
    # Evaluate
    # --------------------------------------------------

    # service = EvaluationService(position)

    result = evaluate_candidate(
        candidate=candidate,
        job_description=job_description,
        position=POSITION
    )

    print("\n" + "=" * 70)
    print("EVALUATION RESULT")
    print("=" * 70)

    pprint(result.model_dump())


if __name__ == "__main__":
    main()