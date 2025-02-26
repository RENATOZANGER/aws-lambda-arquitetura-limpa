import json
from dataclasses import dataclass
from typing import Union, Dict, Any
import boto3
from src.interfaces.secrets_manager_interface import SecretsManagerInterface
from src.utils import LOGGER
from src.utils.enums import AWSRegion
from src.utils.exceptions import GetSecretError


@dataclass
class SecretsManagerAdapter(SecretsManagerInterface):
    secrets_manager = boto3.client('secretsmanager', region_name=AWSRegion.SAO_PAULO.value)
    
    def get_secrets(self, secret_id: str) -> Union[Dict[str, Any], str]:
        try:
            secret_value =  self.secrets_manager.get_secret_value(SecretId=secret_id)
            secret_string = secret_value.get("SecretString")
            
            if self.__is_json_string(secret_string):
                secret_data = json.loads(secret_string)
            else:
                secret_data = secret_string
                
            LOGGER.info(
                log_code="get_Secrets",
                log_message=f"Segredo {secret_id} obtido com sucesso",
                payload=""
            )
            return secret_data
        
        except Exception as e:
            LOGGER.error(
                log_code="get_Secrets",
                log_message=f"Erro ao obter o segredo  {secret_id}: {e}",
                payload=""
            )
        raise GetSecretError(f"Erro ao obter o segredo {secret_id}")
    
    @staticmethod
    def __is_json_string(s: str) -> bool:
        try:
            json_object = json.loads(s)
            return isinstance(json_object, dict)
        except ValueError:
            return False
