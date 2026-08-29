from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.extractor import extract_text
from src.llm.groq import GroqLLM
from src.models import CandidateProfile
from src.parser import Parser


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

CV_PATH = Path("data/cvs")


# ---------------------------------------------------------------------------
# Find CV
# ---------------------------------------------------------------------------

def find_cv() -> Path:
    """
    Find the first supported CV in data/cvs/.
    """

    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
    }

    for path in CV_PATH.iterdir():
        if path.is_file() and path.suffix.lower() in supported_extensions:
            return path

    raise FileNotFoundError(
        f"No supported CV found in {CV_PATH}"
    )


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------

def main() -> None:

    cv_path = find_cv()

    print(f"CV: {cv_path}")
    print()

    # ---------------------------------------------------------------
    # 1. Extract text from CV
    # ---------------------------------------------------------------

    print("Extracting text...")

    document = extract_text(cv_path)

    # print("=" * 70)
    # print("EXTRACTED TEXT")
    # print("=" * 70)
    # print(document.raw_text)
    # print("=" * 70)
    # print()

    # print(
    #     f"Extracted {document.character_count} characters "
    #     f"from {document.page_count} page(s)."
    # )

    print()

    # ---------------------------------------------------------------
    # 2. Initialize Groq
    # ---------------------------------------------------------------

    print("Initializing Groq...")

    llm = GroqLLM()

    # ---------------------------------------------------------------
    # 3. Create parser
    # ---------------------------------------------------------------

    parser = Parser(llm)

    # ---------------------------------------------------------------
    # 4. Parse CV
    # ---------------------------------------------------------------

    print("Parsing CV with Groq...")
    print()

    profile: CandidateProfile = parser.parse_resume(document)

    # ---------------------------------------------------------------
    # 5. Display result
    # ---------------------------------------------------------------

    print("=" * 70)
    print("PARSED CANDIDATE")
    print("=" * 70)

    print(
        json.dumps(
            profile.model_dump(),
            indent=2,
            ensure_ascii=False,
        )
    )

    print()
    print("Parsing completed successfully.")


if __name__ == "__main__":
    main()