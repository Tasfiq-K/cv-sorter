from __future__ import annotations

from pathlib import Path

import pdfplumber
from docx import Document
from . models import CandidateDocument


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class UnsupportedFileTypeError(Exception):
    """Raised when attempting to extract text from an unsupported file type."""


def extract_text(file_path: str | Path) -> str:
    """
    Extract text from a supported document.

    Supported formats:
        - PDF
        - DOCX
        - TXT

    Parameters
    ----------
    file_path : str | Path
        Path to the document.

    Returns
    -------
    str
        Extracted text.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    UnsupportedFileTypeError
        If the file extension is unsupported.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return _extract_pdf(path)

    if extension == ".docx":
        return _extract_docx(path)

    if extension == ".txt":
        return _extract_txt(path)

    raise UnsupportedFileTypeError(
        f"Unsupported file type '{extension}'. "
        f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
    )


def extract_directory(folder: str | Path) -> dict[str, str]:
    """
    Extract text from every supported document inside a directory.

    Returns
    -------
    dict[str, str]

        {
            "john.pdf": "...text...",
            "alice.docx": "...text..."
        }
    """

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(folder)

    documents: list[CandidateDocument] = []

    for file in sorted(folder.iterdir()):
        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            documents.append(extract_text(file))
            # documents[file.name] = extract_text(file)

        except Exception as e:
            print(f"Skipping {file.name}: {e}")

    return documents


# ---------------------------------------------------------------------
# Internal extractors
# ---------------------------------------------------------------------


def _extract_pdf(path: Path) -> str:
    pages: list[str] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                pages.append(text)
    return CandidateDocument(
        filename=path.name,
        path=path,
        extension=path.suffix.lower(),
        raw_text="\n\n".join(pages).strip(),
        page_count=len(pdf.pages),
        character_count=len(text),
    )

def _extract_docx(path: Path) -> str:
    doc = Document(path)

    paragraphs = [
        p.text.strip()
        for p in doc.paragraphs
        if p.text.strip()
    ]

    text = "\n".join(paragraphs)

    return CandidateDocument(
        filename=path.name,
        path=path,
        extension=path.suffix.lower(),
        raw_text=text,
        page_count=1,
        character_count=len(text)
    )



def _extract_txt(path: Path) -> str:
    text = path.read_text(...)

    return CandidateDocument(
        filename=path.name,
        path=path,
        extension=path.suffix.lower(),
        raw_text=text,
        page_count=1,
        character_count=len(text)
    )


if __name__ == "__main__":
    from pprint import pprint
    file_path = "data/cvs/Md Tasfiq Kamran.pdf"
    text = extract_text(file_path)

    pprint(text)
