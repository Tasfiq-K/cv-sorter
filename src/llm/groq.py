from __future__ import annotations

import json
import os

from groq import Groq
from pydantic import BaseModel

from src.llm.base import BaseLLM
from src.llm.prompts import PromptManager
from src.models import Document


class GroqLLM(BaseLLM):
    """
    Groq implementation of the BaseLLM interface.

    Uses Groq Structured Outputs with JSON Schema and
    validates the returned data with Pydantic.
    """

    def __init__(
            self,
            api_key: str | None = None,
            model: str | None = None,
            prompt_manager: PromptManager | None = None

    ):

        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

        self.client = Groq(api_key=self.api_key)

        self.prompt_manager = (
            prompt_manager or PromptManager()
        )


    def extract(
            self,
            document: Document,
            output_model: type[BaseModel],
            prompt_name: str
    ) -> BaseModel:
        """
        Extract structured information from a document.
        """

        prompt = self.prompt_manager.render(
            prompt_name,
            resume_text=document.raw_text,
            document_text=document.raw_text
        )

        schema = output_model.model_json_schema()

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": prompt,
                }
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": self._schema_name(output_model),
                    "strict": True,
                    "schema": schema
                },
            },

            temperature=0
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        data = json.loads(content)

        return output_model.model_validate(data)


    @staticmethod
    def _schema_name(
        output_model: type[BaseModel],
    ) -> str:

        """
        Generate a safe schema name for Groq. 
        """

        return output_model.__name__.lower()