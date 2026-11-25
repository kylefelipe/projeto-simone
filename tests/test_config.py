import pytest

from simone.config import Settings


def test_settings_default_values() -> None:
    config = Settings()

    assert config.ollama_host == "http://127.0.0.1:11434"
    assert config.model == "llama3.2:3b"
    assert config.temperature == 0.1
    assert config.num_predict == 1024

@pytest.mark.parametrize("host", ["", "  "])
def test_settings_reject_empty_host(host: str) -> None:
    with pytest.raises(ValueError):
        Settings(ollama_host=host)

@pytest.mark.parametrize("model", ["", "  "])
def test_settings_rejects_empty_model(model: str) -> None:
    with pytest.raises(ValueError, match="nome do modelo"):
        Settings(model=model)


@pytest.mark.parametrize(
        "temperature",
        [-0.1, float("nan"), float("inf"), float("-inf"), True],
    )
def test_settings_rejects_invalid_temperature(
    temperature: float
) -> None:
    with pytest.raises(ValueError, match="temperatura"):
        Settings(temperature=temperature)


@pytest.mark.parametrize("num_predict", [0, -1, 1.5, True])
def test_settings_rejects_invalid_num_predict(num_predict: int) -> None:
    with pytest.raises(ValueError, match="num_predict"):
        Settings(num_predict=num_predict)
