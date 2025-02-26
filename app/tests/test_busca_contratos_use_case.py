from unittest.mock import MagicMock, patch
import pytest
from tests.fixtures import mock_env_vars, retorno_consulta_bd


class TestCase:
    @pytest.fixture(autouse=True)
    @patch('pymysql.connect')
    def setup(self,mock_criar_conexao, mock_env_vars):
        from src.infra.db_connection import DBConnection
        from src.infra.data_base_manager import DataBaseAdapter
        from src.infra.data_base_manager import DataBaseManager
        
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        
        mock_criar_conexao.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        self.db_connection = DBConnection(secrets_manager=MagicMock())
        self.db = DataBaseAdapter(connection_manager=self.db_connection)
        self.use_case = DataBaseManager(self.db)
        
    def test_busca_conta_com_valor(self, retorno_consulta_bd):
        self.mock_cursor.rowcount = 1
        self.mock_cursor.fetchall.return_value = [retorno_consulta_bd]
        
        contratos = self.use_case.busca_conta(self.mock_cursor)
        assert contratos[0].agencia == '1111'
        
    def test_busca_conta_sem_valor(self):
        self.mock_cursor.rowcount = 0
        self.mock_cursor.fetchall.return_value = []
        
        contratos = self.use_case.busca_conta(self.mock_cursor)
        assert contratos == []
