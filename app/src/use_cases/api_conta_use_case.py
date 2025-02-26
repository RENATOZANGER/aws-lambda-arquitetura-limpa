from dataclasses import dataclass
from src.adapters.api_conta_adapter import ApiContaAdapter


@dataclass
class ApiContaUseCase:
    api_conta_adapter: ApiContaAdapter
    
    def obter_dados_da_conta(self, conta):
        return self.api_conta_adapter.obter_dados_da_conta(conta)
