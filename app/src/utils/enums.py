import os
from enum import Enum


class AWSRegion(Enum):
    SAO_PAULO = "sa-east-1"
    
class Urls(Enum):
    URL_STS = os.environ["URL_STS"]
    URL_GATEWAY_CONTA = os.environ["URL_GATEWAY"] + "v1/conta/"
    

class Credenciais(Enum):
    ARN_CLIENT_ID_CLIENT_SECRET = os.environ["ARN_CLIENT_ID_CLIENT_SECRET"]

class Uteis(Enum):
    TABELA_CONTRATO = "tbjcontrato"
