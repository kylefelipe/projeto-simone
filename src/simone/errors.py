class SimoneError(Exception):
    """Erro base da aplicação Simone."""


class OllamaError(SimoneError):
    """Erro genérico na comunicação com o Ollama."""


class OllamaConnectionError(OllamaError):
    """Não foi possível conectar ao servidor Ollama."""


class OllamaModelError(OllamaError):
    """O Modelo solicitado não está disponível."""
