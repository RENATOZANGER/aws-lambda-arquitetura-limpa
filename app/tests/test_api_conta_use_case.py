import json
from unittest.mock import MagicMock, patch, Mock
import pytest
import requests.exceptions
from src.domain.models.conta_request import ContaRequest
from tests.fixtures import mock_env_vars, mock_requests, solicitar_api_conta, resposta_api_conta, retorno_consulta_bd


class TestProcessaApiContaAdapter:
    @pytest.fixture(autouse=True)
    def setup(self, mock_env_vars, mock_requests, solicitar_api_conta,retorno_consulta_bd):
        self.mock_requests = mock_requests
        self.mock_requests.post(
            "https://mock-sts-url.com",
            json={"access_token": "mock_access_token"},
            status_code=200
        )
        self.conta_completa = retorno_consulta_bd.agencia +retorno_consulta_bd.conta + retorno_consulta_bd.dac
        self.conta_request = ContaRequest(self.conta_completa)
        
        self.parameter_store_mock = MagicMock()
        self.parameter_store_mock.get_value.return_value = "https://mock-api-gateway.com"
        from src.use_cases.api_conta_use_case import ApiContaUseCase
        from src.adapters.api_conta_adapter import ApiContaAdapter
        
        response_conta = ApiContaAdapter(
            client_id_client_secret={'client_id': 'mock', 'client_secret': 'mock'}
        )
        
        self.api_conta_use = ApiContaUseCase(response_conta)
        
    @patch('src.adapters.api_conta_adapter.requests.get')
    def test_processa_api_conta_sucesso(self,mock_get, resposta_api_conta):
        mock_get.return_value.status_code = 200
        json_data = {"data": [resposta_api_conta.__dict__]}
        mock_get.return_value.text = json.dumps(json_data)
        mock_get.return_value.json.return_value = json_data
        
        retorno_conta = self.api_conta_use.obter_dados_da_conta(self.conta_completa)
        
        assert retorno_conta.id_conta == "123"
    
    @patch('src.adapters.api_conta_adapter.requests.get')
    def test_processa_api_conta_sucesso_sem_retorno_conta(self, mock_get):
        mock_get.return_value.status_code = 200
        json_data = {"messages": [{"mensagem": "vazio"}]}
        mock_get.return_value.text = json.dumps(json_data)
        mock_get.return_value.json.return_value = json_data
        
        retorno_conta = self.api_conta_use.obter_dados_da_conta(self.conta_completa)
        
        assert retorno_conta.id_conta == ""
    
    @patch('src.adapters.api_conta_adapter.requests.get')
    def test_processa_api_conta_erro_com_json(self, mock_get):
        mock_get.return_value.status_code = 400
        json_data = {"Error": "error"}
        mock_get.return_value.text = json.dumps(json_data)
        mock_get.return_value.json.return_value = json_data
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()
        
        retorno_conta = self.api_conta_use.obter_dados_da_conta(self.conta_completa)
        
        assert retorno_conta.id_conta == ""
    
    @patch('src.adapters.api_conta_adapter.requests.get')
    def test_processa_api_conta_erro_sem_json(self, mock_get):
        mock_response = Mock()
        mock_get.return_value.status_code = 400
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "not is json", 0)
        mock_response.text = "nao e json"
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.RequestException
        
        retorno_conta = self.api_conta_use.obter_dados_da_conta(self.conta_completa)
        assert retorno_conta.id_conta == ""
