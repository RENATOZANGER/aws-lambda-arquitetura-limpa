from abc import abstractmethod, ABC
from typing import List
from src.domain.models.conta_completa import ContaCompleta


class DataBaseInterface(ABC):
    @abstractmethod
    def busca_conta(self,cursor) -> List[ContaCompleta]:
        pass
    
    @staticmethod
    @abstractmethod
    def atualiza_dados_conta(self, contrato:ContaCompleta, cursor) -> str:
        pass
