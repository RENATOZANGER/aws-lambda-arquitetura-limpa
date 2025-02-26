from dataclasses import dataclass, field
from typing import Optional
import pymysql.cursors
from src.domain.models.conta_completa import ContaCompleta
from src.infra.db_connection import DBConnection
from src.interfaces.database_interface import DataBaseInterface
from src.utils import LOGGER
from src.utils.enums import Uteis
from src.utils.exceptions import DataBaseException


@dataclass
class DataBaseAdapter(DataBaseInterface):
    connection_manager: DBConnection
    conexao: Optional[pymysql.connections.Connection] = field(init=False, default=None)
    
    def __post_init__(self):
        self.conexao = self.connection_manager.cria_conexao()
        LOGGER.info(
            log_code="DataBase",
            log_message="conexao com o Bd criada com sucesso",
            payload=""
        )
        
    def busca_conta(self, cursor) -> [ContaCompleta]:
        try:
            query = f"""
                    SELECT * FROM {Uteis.TABELA_CONTRATO.value} WHERE situacao_conta = 'Cancelada'
                    """
            cursor.execute(query)
            registros = cursor.fetchall()
            if registros:
                LOGGER.info(
                    log_code="busca_conta",
                    log_message=f"Total de registros encontrados:{len(registros)}",
                    payload=""
                )
            else:
                LOGGER.info(
                    log_code="busca_conta",
                    log_message=f"Nenhum registro encontrado",
                    payload=""
                )
            return registros
        
        except Exception as e:
            LOGGER.error(
                log_code="busca_conta",
                log_message=f"Erro ao buscar a conta: {str(e)}",
                payload=""
            )
            raise DataBaseException("Erro ao buscar a conta")
        
    def atualiza_dados_conta(self, contrato: ContaCompleta, cursor):
        try:
            query = f"""
                    UPDATE {Uteis.TABELA_CONTRATO.value}
                    SET
                        data_encerramento = %s,
                        data_abertura = %s,
                        situacao_conta = 'Ativada'
                    WHERE id_conta = %s
                    
                    """
            resultado = cursor.execute(query, (contrato.data_encerramento,contrato.data_abertura,contrato.id_conta))
            if resultado:
                self.conexao.commit()
                LOGGER.info(
                    log_code="atualiza_dados_conta",
                    log_message="contrato atualizado com sucesso",
                    payload=contrato.__dict__
                )
        except Exception as e:
            LOGGER.error(
                log_code="atualiza_dados_conta",
                log_message=f"Erro ao atualizar a conta: {str(e)}",
                payload=contrato.__dict__
            )
            raise DataBaseException("Erro ao atualizar a conta")
