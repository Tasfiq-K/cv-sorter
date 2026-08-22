from __future__ import annotations

import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Main preprocessing pipeline.
    Every parser should call this before attempting 
    any information extraction
    """

    text = normalize_unicode(text)
    text = normalize_line_endings(text)
    text = remove_trailing_whitespace(text)
    text = collapse_multiple_spaces(text)
    text = collapse_blank_lines(text)

    return text.strip()


def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters
    """

    return unicodedata.normalize("NFKC", text)

def normalize_line_endings(text: str) -> str:
    """
    Convert windows/mac line to unix.
    """

    return text.replace("\r\n", "\n").replace("\r", "\n")


def remove_trailing_whitespace(text: str) -> str:
    """
    Remove trailing space from every line
    """

    lines = [line.strip() for line in text.split("\n")]

    return "\n".join(lines)


def collapse_multiple_spaces(text: str) -> str:
    """
    Replace consecutive spaces/tabs with a single space.
    Does not affect newlines.
    """

    return re.sub(r"[ \t]+", " ", text)


def collapse_blank_lines(text: str, max_blank_lines: int = 1) -> str:
    """
    Reduce multiple blank lines
    """

    pattern = r"\n{" + str(max_blank_lines + 2) + r",}"
    replacement = "\n" * (max_blank_lines + 1)

    return re.sub(pattern, replacement, text)


if __name__ == "__main__":
    from pathlib import Path

    from src.extractor import extract_text

    cv_path = Path("data/cvs/Md Tasfiq Kamran.pdf")

    document = extract_text(cv_path)

    print("=" * 70)
    print("RAW TEXT")
    print("=" * 70)
    print(document.raw_text)

    print()
    print("=" * 70)
    print("PREPROCESSED TEXT")
    print("=" * 70)

    cleaned_text = clean_text(document.raw_text)

    print(cleaned_text)
    print("=" * 70)