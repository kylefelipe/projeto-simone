import ollama

from simone.config import settings
from simone.errors import OllamaConnectionError, OllamaError, OllamaModelError


class Ollamaclient:
    """Cliente para comunicação com o servidor local do Ollama."""

    def __init__(self) -> None:
        self.client = ollama.Client(
            host=settings.ollama_host,
        )
        self.model = settings.model

    def chat(self, messages: list[dict[str, str]]) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options={
                    "temperature": settings.temperature,
                    "num_predict": settings.num_predict,
                },
            )
            return response.message.content

        except ConnectionError as e:
            raise OllamaConnectionError(
                "Não foi possível conectar ao servidor Ollama. "
                "Verifique se o serviço está em execução."
            ) from e

        except ollama.ResponseError as e:
            if e.status_code == 404:
                raise OllamaModelError(
                    f"Modelo '{self.model}' não encontrado. "
                    "Verifique se ele está instalado no Ollama."
                ) from e

            raise OllamaError(f"Ollama retornou um erro: {e.error}") from e
