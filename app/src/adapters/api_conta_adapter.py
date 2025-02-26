import json
import uuid
from dataclasses import dataclass, field
from typing import Dict
import requests
from src.adapters.token_sts_adapter import StsTokenAdapter
from src.domain.models.conta_response import ContaResponse
from src.interfaces.api_conta_interface import ApiContaInterface
from src.use_cases.get_sts_token_use_case import GetStsTokenUseCase
from src.utils import LOGGER
from src.utils.enums import Urls


@dataclass
class ApiContaAdapter(ApiContaInterface):
    client_id_client_secret: Dict[str, str]
    url_contas: str = Urls.URL_GATEWAY_CONTA.value
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    api_key: str = field(init=False)
    sts_token: str = field(init=False)
    
    def __post_init__(self):
        self.api_key = self.client_id_client_secret['client_id']
        self.sts_token = self.get_sts_token(self.client_id_client_secret)
        
    def obter_dados_da_conta(self, conta) -> ContaResponse:
        try:
            response = self.__executa_request(conta)
            return self.__processa_response(response)
        except requests.exceptions.RequestException as e:
            return self.__trata_excessao(e, conta)
        
    def __executa_request(self, conta) -> requests.Response:
        LOGGER.info(
            log_code="__executa_request",
            log_message="Payload request",
            payload={"conta": conta}
        )
        response = self.__get_request(conta)
        response.raise_for_status()
        return response
    
    def __get_request(self, conta) -> requests.Response:
        return requests.get(
            url=self.url_contas + conta,
            headers=self.__formata_headers()
        )
    
    @staticmethod
    def __processa_response(response) -> ContaResponse:
        LOGGER.info(
            log_code="__processa_response",
            log_message="Retorno da api de contas",
            payload=json.loads(response.text)
        )
        data = response.json().get('data')
        if data:
            contas = [ContaResponse(**conta_data) for conta_data in data]
            return contas[0]
        return ContaResponse(
            id_conta="",agencia="",conta="",dac="",nome_completo="", data_encerramento="",data_abertura=""
        )
    
    def __trata_excessao(self, exception, conta) -> ContaResponse:
        json_error = self.__trata_erro(exception.response, exception)
        LOGGER.error(
            log_code="__trata_excessao",
            log_message="Erro ao obter os dados da conta",
            payload=f"Erro: {json_error}"
        )
        
        if exception.response is not None and exception.response.status_code == 403:
            return self.__busca_novo_token(json_error, conta)
        return ContaResponse(
            id_conta="",agencia="",conta="",dac="",nome_completo="",data_encerramento="",data_abertura=""
        )
    
    def __busca_novo_token(self, json_error, conta) -> ContaResponse:
        LOGGER.warn(
            log_code="__busca_novo_token",
            log_message="Token expirado, obtendo novo token",
            payload=f"Erro: {json_error}"
        )
        self.sts_token = self.get_sts_token(self.client_id_client_secret)
        try:
            response = self.__executa_request(conta)
            return self.__processa_response(response)
        except requests.exceptions.RequestException:
            return ContaResponse(
                id_conta="",agencia="",conta="",dac="",nome_completo="",data_encerramento="",data_abertura=""
            )
        
    def __formata_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.sts_token}",
            "Content-Type": "application/json",
            "x-apikey": self.api_key,
            "x-correlationId": self.correlation_id
        }
    
    def get_sts_token(self, secrets: Dict[str,str]) -> str:
        get_sts_token_use_case = GetStsTokenUseCase(
            token_sts_adapter=StsTokenAdapter()
        )
        return get_sts_token_use_case.get_token_sts(secrets["client_id"], secrets["client_secret"])
    
    @staticmethod
    def __trata_erro(response, exception) -> str:
        if response is not None and response.content:
            try:
                return response.json()
            except ValueError:
                return response.text
        return str(exception)
