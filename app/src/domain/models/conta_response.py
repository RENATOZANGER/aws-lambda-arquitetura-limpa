from dataclasses import dataclass
from typing import Optional


@dataclass
class ContaResponse:
    id_conta: str
    agencia: str
    conta: str
    dac: str
    nome_completo: str
    data_encerramento: str
    data_abertura: str
