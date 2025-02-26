from dataclasses import dataclass
from typing import Dict
import requests.exceptions
from src.interfaces.sts_token_interface import StsTokenInterface
from src.utils import LOGGER
from src.utils.enums import Urls
from src.utils.exceptions import StsError


@dataclass
class StsTokenAdapter(StsTokenInterface):
    @staticmethod
    def get_token_sts(client_id: str, client_secret: str) -> str:
        try:
            return StsTokenAdapter.__request_token(client_id, client_secret)
        except requests.exceptions.RequestException as e:
            if e.response.status_code == requests.codes.unauthorized:
                LOGGER.error(
                    log_code="get_token_sts",
                    log_message="Token invalido",
                    payload=str(e)
                )
                raise StsError(f"Erro ao buscar o token STS: {e}")
    
    @staticmethod
    def __request_token(client_id: str, client_secret: str) -> str:
        response = requests.post(
            url=Urls.URL_STS.value,
            auth=(client_id, client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data= StsTokenAdapter.__data(client_id, client_secret)
        )
        response.raise_for_status()
        LOGGER.info(
            log_code="__request_token",
            log_message="Token obtido com sucesso",
            payload=""
        )
        return response.json()["access_token"]
    
    @staticmethod
    def __data(client_id: str, client_secret: str) -> Dict[str, str]:
        return {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
