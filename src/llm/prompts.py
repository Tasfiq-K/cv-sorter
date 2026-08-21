from __future__ import annotations

from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class PromptManager:
    """
    Loads and renders LLM prompt templates.
    """

    def __init__(self, prompts_dir: Path | None = None):
        self.prompts_dir = prompts_dir or PROMPTS_DIR

    def load(self, prompt_name: str) -> str:
        """
        Load a prompt template by name.

        Example:
            load("cv_parser")
            -> src/prompts/cv_parser.md
        """

        prompt_path = self.prompts_dir / f"{prompt_name}.md"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt not found: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8")

    def render(
        self,
        prompt_name: str,
        **variables: str,
    ) -> str:
        """
        Load a prompt and replace template variables.

        Example template:

            Resume:
            {{resume_text}}

        Example usage:

            manager.render(
                "cv_parser",
                resume_text=text,
            )
        """

        template = self.load(prompt_name)

        for key, value in variables.items():
            template = template.replace(
                "{{" + key + "}}",
                value,
            )

        return template