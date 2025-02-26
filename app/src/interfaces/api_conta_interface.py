from abc import abstractmethod, ABC
from typing import Dict
from src.domain.models.conta_response import ContaResponse


class ApiContaInterface(ABC):
    @abstractmethod
    def obter_dados_da_conta(self,conta_contratual) -> ContaResponse:
        pass
    
    @staticmethod
    @abstractmethod
    def get_sts_token(secrets: Dict[str,str]) -> str:
        pass
