from unittest.mock import MagicMock, patch
import pytest
from tests.fixtures import mock_env_vars, resposta_api_conta


class TestCase:
    @pytest.fixture(autouse=True)
    @patch('pymysql.connect')
    def setup(self, mock_criar_conexao, mock_env_vars, resposta_api_conta):
        from src.infra.db_connection import DBConnection
        from src.infra.data_base_manager import DataBaseAdapter
        from src.infra.data_base_manager import DataBaseManager
        
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        
        mock_criar_conexao.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        self.db_connection = DBConnection(secrets_manager=MagicMock())
        self.db = DataBaseAdapter(connection_manager=self.db_connection)
        self.atualizar_conta_adapter = DataBaseManager(self.db)
    
    def test_atualiza_conta_com_contrato(self, resposta_api_conta):
        self.mock_cursor.execute.return_value = 1
        
        resultado = self.atualizar_conta_adapter.atualiza_dados_conta(resposta_api_conta, self.mock_cursor)
        assert resultado is None
    
    def test_atualiza_conta_nao_encontrou(self, resposta_api_conta):
        self.mock_cursor.execute.return_value = 0
        
        resultado = self.atualizar_conta_adapter.atualiza_dados_conta(resposta_api_conta, self.mock_cursor)
        assert resultado is None
    
    def test_atualiza_conta_com_erro(self, resposta_api_conta):
        self.mock_cursor.execute.side_effect = Exception("Erro SQL")
        
        with pytest.raises(Exception):
            self.atualizar_conta_adapter.atualiza_dados_conta(resposta_api_conta, self.mock_cursor)
