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
    pass           


def normalize_line_endings(text: str) -> str:
    pass


def remove_trailing_whitespace(text: str) -> str:
    pass


def collapse_multiple_spaces(text: str) -> str:
    pass


def collapse_blank_lines(text: str) -> str:
    pass