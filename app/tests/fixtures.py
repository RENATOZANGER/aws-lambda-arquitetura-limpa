import pytest
from src.domain.models.conta_completa import ContaCompleta
from src.domain.models.conta_request import ContaRequest
from src.domain.models.conta_response import ContaResponse


@pytest.fixture
def solicitar_api_conta():
    return ContaRequest(
        conta_completa="123412345678"
    )

@pytest.fixture
def resposta_api_conta():
    return ContaResponse(
        id_conta= "123",
        agencia= "1111",
        conta= "1111111",
        dac= "1",
        nome_completo= "Teste",
        data_encerramento= "12-12-2025",
        data_abertura="01-01-2026"
    )

@pytest.fixture
def retorno_consulta_bd():
    return ContaCompleta(
        id_conta= "123",
        agencia= "1111",
        conta= "1111111",
        dac= "1",
        nome_completo= "Teste",
        data_encerramento= "12-12-2025",
        data_abertura="01-01-2026"
    )

@pytest.fixture
def mock_requests():
    import requests_mock
    with requests_mock.Mocker() as m:
        yield m
        
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("ARN_CLIENT_ID_CLIENT_SECRET", "arn:aws:secretsmanager:sa-east-1:123456789012:secret:secret")
    monkeypatch.setenv("DB_HOST", "arn:aws:secretsmanager:sa-east-1:123456789012:secret:host")
    monkeypatch.setenv("DB_USERNAME", "arn:aws:secretsmanager:sa-east-1:123456789012:secret:username")
    monkeypatch.setenv("DB_PASSWORD", "arn:aws:secretsmanager:sa-east-1:123456789012:secret:pass")
    
    monkeypatch.setenv("URL_GATEWAY", "https://mock-api-gateway.com")
    monkeypatch.setenv("URL_STS", "https://mock-sts-url.com")
    monkeypatch.setenv("CONTA_GATEWAY_ID", "123")
