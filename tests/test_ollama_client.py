from types import SimpleNamespace

import ollama
import pytest

from simone import ollama_client
from simone.errors import OllamaConnectionError, OllamaError, OllamaModelError


class FakeOllamaClient:
    """Simula o cliente SDK do Ollama."""

    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.call_args = None

    def chat(self, **kwargs):
        self.call_args = kwargs

        if self.error:
            raise self.error

        return self.response


def create_client(monkeypatch, fake_client):
    """Cria OllamaClient usando um cliente falso."""
    monkeypatch.setattr(
        ollama_client.ollama,
        "Client",
        lambda host: fake_client,
    )

    return ollama_client.Ollamaclient()


def test_chat_return_response(monkeypatch):
    expected = "Texto Revisado"

    fake_client = FakeOllamaClient(
        response=SimpleNamespace(message=SimpleNamespace(content=expected))
    )

    client = create_client(monkeypatch, fake_client)

    messages = [
        {"role": "system", "content": "Você é um revisor."},
        {"role": "user", "content": "Texto original"},
    ]

    result = client.chat(messages)

    assert result == expected
    assert fake_client.call_args is not None
    assert fake_client.call_args["model"] == client.model
    assert fake_client.call_args["messages"] == messages
    assert fake_client.call_args["stream"] is False


def test_chat_handles_connection_error(monkeypatch):
    fake_client = FakeOllamaClient(error=ConnectionError("Connection refused"))

    client = create_client(monkeypatch=monkeypatch, fake_client=fake_client)

    with pytest.raises(OllamaConnectionError) as e_info:
        client.chat([])

    assert "servidor Ollama" in str(e_info)
    assert isinstance(e_info.value.__cause__, ConnectionError)


def test_chat_handles_model_not_found(monkeypatch):
    fake_client = FakeOllamaClient(
        error=ollama.ResponseError("model not found", status_code=404)
    )

    client = create_client(monkeypatch=monkeypatch, fake_client=fake_client)

    with pytest.raises(OllamaModelError) as e_info:
        client.chat([])

    assert client.model in str(e_info.value)
    assert "não encontrado" in str(e_info.value)
    assert isinstance(e_info.value.__cause__, ollama.ResponseError)


def test_chat_handles_generic_response_error(monkeypatch):
    fake_client = FakeOllamaClient(
        error=ollama.ResponseError("Internal server error", status_code=500)
    )

    client = create_client(monkeypatch=monkeypatch, fake_client=fake_client)

    with pytest.raises(OllamaError) as exc_info:
        client.chat([])

    assert "Internal server error" in str(exc_info.value)
    assert not isinstance(exc_info.value, OllamaModelError)
