from simone.reviewer import Reviewer


class FakeOllamaClient:
    """Simula o cliente do Ollama sem acessar a rede."""

    def __init__(self, response: str = "") -> None:
        self.response = response
        self.messages = None
        self.called = False

    def chat(self, messages: list[dict[str, str]]) -> str:
        self.called = True
        self.messages = messages
        return self.response


def test_review_corrects_grammar_without_changing_person() -> None:
    original = "Eu não sabia que eles estava aqui."
    expected = "Eu não sabia que eles estavam aqui."

    client = FakeOllamaClient(response=expected)
    reviewer = Reviewer(client=client)

    result = reviewer.review(original)

    assert result == expected
    assert client.called
    assert client.messages is not None
    assert client.messages[-1] == {"role": "user", "content": original}


def test_review_sends_system_prompt() -> None:
    client = FakeOllamaClient(response="Texto revisado.")
    reviewer = Reviewer(client=client)

    reviewer.review("Texto original")

    assert client.messages is not None
    system_message = client.messages[0]

    assert system_message["role"] == "system"
    assert "pessoa gramatical" in system_message["content"]
    assert "exclusivamente o texto revisado" in (system_message["content"]).lower()


def test_review_rejects_empty_text() -> None:
    client = FakeOllamaClient()
    reviewer = Reviewer(client=client)

    try:
        reviewer.review("  ")
    except ValueError as e:
        assert str(e) == "O texto para revisão não pode estar vazio."
    else:
        raise AssertionError("Era esperada uma exceção ValueError.")

    assert not client.called
