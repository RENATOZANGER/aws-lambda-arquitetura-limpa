from dataclasses import dataclass
from src.adapters.processa_contratos_adapter import ProcessaContratosAdapter


@dataclass
class ProcessaContratoUseCase:
    processa_contratos_adapter: ProcessaContratosAdapter
    
    def processa_contrato(self):
        return self.processa_contratos_adapter.processa_contrato()
