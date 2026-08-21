from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar
from pydantic import BaseModel

from src.models import Document


T = TypeVar("T", bound=BaseModel)


class BaseLLM(ABC):
    """
    Abstract interface for LLM-based structured extraction.

    Providers such as OpenAI and Ollama implement this interface.
    The rest of the application does not need to know which provider
    is being used.
    """

    @abstractmethod
    def extract(
        self, 
        document: Document,
        output_model: type[T],
        promt_name: str
    ) -> T:

        """
        Extract structured information from a document.

        Parameters
        ----------
        document:
            The preprocessed document.

        output_model:
            Pydantic model describing the expected output.

        prompt_name:
            Name of the prompt/template to use.

        Returns
        -------
        T:
            A validated instance of output_model.
        """
        raise NotImplementedError

