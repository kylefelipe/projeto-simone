import math
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_host: str = "http://127.0.0.1:11434"
    model: str = "llama3.2:3b"
    temperature: float = 0.1
    num_predict: int = 1024


    def __post_init__(self) -> None:
        if not self.ollama_host.strip():
            raise ValueError("O endereço do Ollama não pode ser vazio.")

        if not self.model.strip():
            raise ValueError("O nome do modelo não pode ser vazio.")

        if (
            isinstance(self.temperature, bool)
            or not isinstance(self.temperature, (int, float))
            or not math.isfinite(self.temperature)
            or self.temperature < 0
        ):
            raise ValueError(
                "A temperatura deve ser um número finito maior ou igual a zero"
            )


        if (
            isinstance(self.num_predict, bool)
            or not isinstance(self.num_predict, int)
            or self.num_predict <= 0
        ):
            raise ValueError(
                "num_predict deve ser um número inteiro maior que zero."
            )


settings = Settings(
    ollama_host=os.getenv("SIMONE_OLLAMA_HOST", "http://127.0.0.1:11434"),
    model=os.getenv("SIMONE_MODEL", "llama3.2:3b"),
    temperature=float(os.getenv("SIMONE_TEMPERATURE", "0.1")),
    num_predict=int(os.getenv("SIMONE_NUM_PREDICT", "1024")),
)
