from pathlib import Path

from simone.ollama_client import Ollamaclient

PROMPT_PATH = Path(__file__).parent / "prompts" / "revisar.md"


class Reviewer:
    """Revisa textos usando um modelo local."""

    def __init__(self, client: Ollamaclient | None = None) -> None:
        self.client = client or Ollamaclient()
        self.system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    def review(self, text: str) -> str:
        """Retorna uma versão revisada do texto informado."""

        if not text.strip():
            raise ValueError("O texto para revisão não pode estar vazio.")

        return self.client.chat(
            [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text},
            ]
        )
