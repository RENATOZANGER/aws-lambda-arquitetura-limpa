from dataclasses import dataclass


@dataclass
class ContaCompleta:
    id_conta: str
    agencia: str
    conta: str
    dac: str
    data_encerramento: str
    data_abertura: str
    nome_completo: str
