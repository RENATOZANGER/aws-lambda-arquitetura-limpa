from dataclasses import dataclass, field
from src.adapters.api_conta_adapter import ApiContaAdapter
from src.adapters.database_adapter import DataBaseAdapter
from src.domain.models.conta_completa import ContaCompleta
from src.domain.models.conta_request import ContaRequest
from src.infra.data_base_manager import DataBaseManager
from src.interfaces.processa_contrato_interface import ProcessaContratoInterface
from src.use_cases.api_conta_use_case import ApiContaUseCase


@dataclass
class ProcessaContratosAdapter(ProcessaContratoInterface):
    api_conta_adapter: ApiContaAdapter
    database_adapter: DataBaseAdapter
    api_conta_use_case: ApiContaUseCase = field(init=False)
    database_base_manager: DataBaseManager = field(init=False)
    
    def __post_init__(self):
        self.api_conta_use_case = ApiContaUseCase(api_conta_adapter=self.api_conta_adapter)
        self.database_base_manager = DataBaseManager(database_adapter=self.database_adapter)
        
        
    def processa_contrato(self):
        with self.database_adapter.conexao.cursor() as cursor:
            contratos = self.database_base_manager.busca_conta(cursor)
            
            for contrato in contratos:
                agencia_conta_dac = self.__conta_completa(contrato)
                retorno_api = self.api_conta_use_case.obter_dados_da_conta(agencia_conta_dac)
                if retorno_api.id_conta:
                    self.database_base_manager.atualiza_dados_conta(self.__atualizar_conta(retorno_api),cursor)
                
                
    @staticmethod
    def __conta_completa(contrato):
        return ContaRequest(
            conta_completa=contrato["agencia"] + contrato["conta"] + contrato["dac"]
            )
    
    @staticmethod
    def __atualizar_conta(contrato):
        return ContaCompleta(
            id_conta=contrato.id_conta,
            agencia=contrato.agencia,
            conta=contrato.conta,
            dac=contrato.dac,
            data_encerramento=contrato.data_encerramento,
            data_abertura=contrato.data_abertura,
            nome_completo=contrato.nome_completo
        )
