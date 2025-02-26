import pytest
from unittest.mock import MagicMock, patch, Mock
from src.domain.models.conta_request import ContaRequest
from tests.fixtures import mock_env_vars, mock_requests, solicitar_api_conta, resposta_api_conta, retorno_consulta_bd


class TestProcessaContratosAdapter:
    @pytest.fixture(autouse=True)
    def setup(self, mock_env_vars, mock_requests, solicitar_api_conta, resposta_api_conta):
        self.resposta_api_conta = resposta_api_conta
        self.mock_requests = mock_requests
        self.mock_requests.post(
            "https://mock-sts-url.com",
            json={"access_token": "mock_access_token"},
            status_code=200
        )
        self.conta = solicitar_api_conta.__dict__
        self.conta_request = ContaRequest(self.conta.get('conta_completa'))

        self.parameter_store_mock = MagicMock()
        self.parameter_store_mock.get_value.return_value = "https://mock-api-gateway.com"

        from src.adapters.api_conta_adapter import ApiContaAdapter
        self.api_conta_adapter = MagicMock(spec=ApiContaAdapter)
        self.api_conta_adapter.obter_dados_da_conta.return_value = self.resposta_api_conta
    
    @patch('src.adapters.processa_contratos_adapter.DataBaseAdapter')
    @patch('src.use_cases.get_sts_token_use_case.GetStsTokenUseCase.get_token_sts')
    def test_processa_contratos(self, mock_token, mock_data_base_adapter, retorno_consulta_bd):
        mock_instance = mock_token.return_value
        mock_instance.execute.return_value = "mock_token"
        
        # Mock do DatabaseAdapter
        mock_database_adapter = mock_data_base_adapter()
        mock_database_adapter.conexao = Mock()
        
        # Mock do cursor
        mock_instance = mock_token.return_value
        mock_instance.execute.return_value = "mock_token"
        
        mock_database_adapter = mock_data_base_adapter()
        mock_database_adapter.conexao = Mock()
        
        mock_database_adapter.conexao.__enter__ = Mock(return_value=mock_database_adapter.conexao)
        mock_database_adapter.conexao.__exit__ = Mock(return_value=None)
        
        mock_cursor = Mock()
        mock_database_adapter.conexao.cursor.return_value = mock_cursor
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=None)
        
        # Simula o retorno do banco de dados
        mock_database_adapter.busca_conta.return_value = [
            retorno_consulta_bd.__dict__
        ]
        
        from src.adapters.processa_contratos_adapter import ProcessaContratosAdapter
        from src.use_cases.processa_contrato_use_case import ProcessaContratoUseCase
        
        processa_contratos_adapter = ProcessaContratosAdapter(
            database_adapter=mock_database_adapter,
            api_conta_adapter=self.api_conta_adapter
        )
        
        processa_contrato_use_case = ProcessaContratoUseCase(
            processa_contratos_adapter=processa_contratos_adapter
        )
        
        processa_contrato_use_case.processa_contrato()
