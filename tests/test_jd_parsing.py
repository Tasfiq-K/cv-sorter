from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.extractor import extract_text
from src.llm.groq import GroqLLM
from src.models import JobDescription
from src.parser import Parser


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

JD_PATH = Path("data/job_descriptions")


# ---------------------------------------------------------------------------
# Find JD
# ---------------------------------------------------------------------------

def find_jd() -> Path:
    """
    Find the first supported JD in data/job_descriptions/.
    """

    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
        ".md"
    }

    for path in JD_PATH.iterdir():
        if path.is_file() and path.suffix.lower() in supported_extensions:
            return path

    raise FileNotFoundError(
        f"No supported CV found in {JD_PATH}"
    )


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------

def main() -> None:

    jd_path = find_jd()

    print(f"CV: {jd_path}")
    print()

    # ---------------------------------------------------------------
    # 1. Extract text from CV
    # ---------------------------------------------------------------

    print("Extracting text...")

    document = extract_text(jd_path)

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
    # 4. Parse JD
    # ---------------------------------------------------------------

    print("Parsing JD with Groq...")
    print()

    profile: JobDescription = parser.parse_jd(document)

    # ---------------------------------------------------------------
    # 5. Display result
    # ---------------------------------------------------------------

    print("=" * 70)
    print("PARSED Job Description")
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