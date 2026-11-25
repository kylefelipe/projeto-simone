import argparse
import sys
from pathlib import Path

from simone.errors import OllamaConnectionError, OllamaError, OllamaModelError
from simone.reviewer import Reviewer


def revisar(args: argparse.Namespace) -> int:
    """Lê um texto e imprime sua versão revisada."""
    if args.arquivo:
        try:
            text = Path(args.arquivo).read_text(encoding="utf-8")
        except OSError as e:
            print(f"Erro ao ler o arquivo: {e}", file=sys.stderr)
            return 1
    else:
        if sys.stdin.isatty():
            print(
                "informe um arquivo ou envie o texto pela entrada padrão.",
                file=sys.stderr,
            )
            return 2
        text = sys.stdin.read()

    try:
        reviewer = Reviewer()
        resultado = reviewer.review(text)
    except ValueError as exc:
        print(f"Erro {exc}", file=sys.stderr)
        return 2

    except OllamaConnectionError as e:
        print(f"Erro de conexão: {e}", file=sys.stderr)
        return 1

    except OllamaModelError as e:
        print(f"Erro de Modelo {e}", file=sys.stderr)
        return 1

    except OllamaError as e:
        print(f"Erro no Ollama: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Erro inesperado {e}", file=sys.stderr)
        return 1

    print(resultado)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Simone", description="Assistente local para revisão e análise de textos."
    )

    subparsers = parser.add_subparsers(dest="comando", required=True)

    parser_revisar = subparsers.add_parser(
        "revisar", help="Revisa um texto em portugês brasileiro."
    )

    parser_revisar.add_argument(
        "arquivo",
        nargs="?",
        help="Arquivo de texto UTF-8. Se omitido, lê a entrada padrão.",
    )

    parser_revisar.set_defaults(func=revisar)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
