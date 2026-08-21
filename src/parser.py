from __future__ import annotations

from src.llm.base import BaseLLM

from src.models import (
    Document,
    CandidateDocument,
    CandidateProfile,
    JobDescription,
    JobDescriptionDocument
)

from src.parsers.preprocess import clean_text


class Parser:
    """
    High-level parser that orchestrates document parsing.

    Responsibilities:
        1. Clean extracted text
        2. Delegate parsing to the configured LLM
        3. Return validated models
    """

    def __init__(self, llm: BaseLLM):
        self.llm = llm


    def _prepare(self, document: Document) -> Document:
        """
        Preprocess a document before sending to the LLM
        """

        cleaned_text = clean_text(document.raw_text)

        return document.model_copy(
            update={
                'raw_text': cleaned_text,
                'character_count': len(cleaned_text)
            }
        )

    
    def parse_resume(
            self, 
            document: CandidateDocument,
    ) -> CandidateProfile:

        doc = self._prepare(document)

        return self.llm.parse_resume(doc)


    def parse_jd(
            self, 
            document: JobDescriptionDocument
    ) -> JobDescription:

        doc = self._prepare(document)

        return self.llm.parse_jd(doc)