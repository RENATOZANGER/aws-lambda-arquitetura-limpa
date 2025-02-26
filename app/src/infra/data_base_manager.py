from dataclasses import dataclass
from src.adapters.database_adapter import DataBaseAdapter
from src.domain.models.conta_completa import ContaCompleta

@dataclass
class DataBaseManager:
    database_adapter: DataBaseAdapter
    
    def busca_conta(self, cursor):
        return self.database_adapter.busca_conta(cursor)
    
    def atualiza_dados_conta(self, contrato:ContaCompleta, cursor):
        self.database_adapter.atualiza_dados_conta(contrato=contrato, cursor=cursor)
