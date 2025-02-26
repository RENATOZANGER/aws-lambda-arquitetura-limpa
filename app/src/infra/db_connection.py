import os
from dataclasses import dataclass
import pymysql.connections
from src.use_cases.get_secrets_manager_use_case import GetSecretsManagerUseCase
import pymysql.cursors
from src.utils import LOGGER
from src.utils.exceptions import DataBaseException


@dataclass
class DBConnection:
    secrets_manager: GetSecretsManagerUseCase
    dbname: str = "dbcontas"
    port: int = 8036
    
    def cria_conexao(self) -> pymysql.connections.Connection:
        try:
            return pymysql.connect(
                host=self.secrets_manager.get_secrets(os.environ.get("DB_HOST")),
                user=self.secrets_manager.get_secrets(os.environ.get("DB_USERNAME")),
                passwd=self.secrets_manager.get_secrets(os.environ.get("DB_PASSWORD")),
                db=self.dbname,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            LOGGER.error(
                log_code="cria_conexao",
                log_message="Erro ao conectar no banco",
                payload=f"Erro: {e}"
            )
            raise DataBaseException("Erro ao conectar no BD")
