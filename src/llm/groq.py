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
            prompt_manager
            if prompt_manager is not None
            else PromptManager()
        )


    def extract(
            self,
            document: Document,
            output_model: type[BaseModel],
            prompt_name: str
    ) -> BaseModel:
        """
        Extract structured information from a document.

        Parameters
        ----------
        document:
            Preprocessed document containing raw text.

        output_model:
            Pydantic model describing the expected output.

        prompt_name:
            Name of the prompt template without the .md extension.

        Returns
        -------
        BaseModel
            Validated instance of output_model.
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
                    "role": "user",
                    "content": (
                        f"{prompt}\n\n"
                        "Here is the resume to extract:\n\n"
                        f"{document.raw_text}"
                    ),
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": self._schema_name(output_model),
                    "strict": True,
                    "schema": schema,
                },
            },
            reasoning_effort="low",
            max_completion_tokens=4096,
        )

        content = response.choices[0].message.content
        # print("*" * 70)
        # print(content)

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        try: 
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Groq returned invalid JSON."
            ) from exc

        try:
            return output_model.model_validate(data)
        except Exception as exc:
            raise ValueError(
                f"Groq response failed Pydantic validation "
                f"for {output_model.__name__}."
            ) from exc


    @staticmethod
    def _schema_name(
        output_model: type[BaseModel],
    ) -> str:

        """
        Generate a safe schema name for Groq. 
        """

        return output_model.__name__.lower()