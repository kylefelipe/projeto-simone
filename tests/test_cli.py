from argparse import Namespace
from io import StringIO
from unittest.mock import Mock

import pytest

from simone import cli
from simone.errors import (
    OllamaConnectionError,
    OllamaError,
    OllamaModelError,
)


class FakeReviewer:
    def review(self, text: str) -> str:
        return text.replace("estava", "estavam")


class FailingReviewer:
    def __init__(self, error: Exception) -> None:
        self.error = error

    def review(self, text: str) -> str:
        raise self.error


def test_revisar_reads_stdin(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "Reviewer", FakeReviewer)
    monkeypatch.setattr(
        cli.sys,
        "stdin",
        StringIO("Eu não sabia que eles estava aqui."),
    )

    args = Namespace(arquivo=None)

    result = cli.revisar(args)

    assert result == 0
    assert capsys.readouterr().out == ("Eu não sabia que eles estavam aqui.\n")


def test_revisar_reads_file(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "Reviewer", FakeReviewer)

    arquivo = tmp_path / "texto.txt"
    texto_original = "Eu não sabia que eles estava aqui."

    arquivo.write_text(texto_original, encoding="utf-8")

    args = Namespace(arquivo=str(arquivo))

    result = cli.revisar(args)

    assert result == 0
    assert capsys.readouterr().out == ("Eu não sabia que eles estavam aqui.\n")
    assert arquivo.read_text(encoding="utf-8") == texto_original


def test_revisar_file_not_found(monkeypatch, capsys, tmp_path) -> None:
    arquivo = tmp_path / "inexistente.txt"
    args = Namespace(arquivo=str(arquivo))

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert "Erro ao ler o arquivo:" in captured.err


def test_revisar_file_read_error(monkeypatch, capsys) -> None:
    def raise_permission_error(*args, **kwargs):
        raise PermissionError("Permissão negada")

    monkeypatch.setattr(
        cli.Path,
        "read_text",
        raise_permission_error,
    )

    args = Namespace(arquivo="restrito.txt")

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert "Permissão negada" in captured.err


def test_revisar_interactive_without_file(monkeypatch, capsys) -> None:
    stdin = Mock()
    stdin.isatty.return_value = True

    monkeypatch.setattr(cli.sys, "stdin", stdin)

    args = Namespace(arquivo=None)

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert "informe um arquivo" in captured.err


def test_revisar_empty_stdin(monkeypatch, capsys) -> None:
    error_text = "O texto para revisão não pode estar vazio."

    class EmptyAwareFakeReviewer:
        def review(self, text: str) -> str:
            if not text.strip():
                raise ValueError(error_text)
            return text

    monkeypatch.setattr(cli, "Reviewer", EmptyAwareFakeReviewer)
    monkeypatch.setattr(cli.sys, "stdin", StringIO("  \n"))

    args = Namespace(arquivo=None)

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert error_text in captured.err


@pytest.mark.parametrize(
    ("error", "expected_message"),
    [
        (
            OllamaConnectionError("Servidor indisponível"),
            "Erro de conexão:",
        ),
        (
            OllamaModelError("Modelo não encontrado"),
            "Erro de Modelo",
        ),
        (
            OllamaError("Falha na API"),
            "Erro no Ollama:",
        ),
    ],
)
def test_revisar_handles_ollama_errors(
    monkeypatch,
    capsys,
    error,
    expected_message,
) -> None:
    monkeypatch.setattr(
        cli,
        "Reviewer",
        lambda: FailingReviewer(error),
    )
    monkeypatch.setattr(
        cli.sys,
        "stdin",
        StringIO("Texto para revisar."),
    )

    args = Namespace(arquivo=None)

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert expected_message in captured.err


def test_revisar_handles_unexpected_error(
    monkeypatch,
    capsys,
) -> None:
    error = RuntimeError("Erro inesperado")

    monkeypatch.setattr(
        cli,
        "Reviewer",
        lambda: FailingReviewer(error),
    )
    monkeypatch.setattr(
        cli.sys,
        "stdin",
        StringIO("Texto para revisar."),
    )

    args = Namespace(arquivo=None)

    result = cli.revisar(args)

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert "Erro inesperado" in captured.err


def test_main_calls_revisar(monkeypatch) -> None:
    expected_args = Namespace(arquivo="texto.txt")
    revisar_mock = Mock(return_value=0)

    monkeypatch.setattr(cli.sys, "argv", ["simone", "revisar", "texto.txt"])

    monkeypatch.setattr(
        cli,
        "revisar",
        revisar_mock,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 0
    revisar_mock.assert_called_once()

    received_args = revisar_mock.call_args.args[0]

    assert received_args.arquivo == expected_args.arquivo


def test_main_requires_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli.sys, "argv", ["simone"])

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 2
    assert "usage:" in captured.err
    assert "required" in captured.err
