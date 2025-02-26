from abc import ABC


class StsTokenInterface(ABC):
    @staticmethod
    def get_token_sts(client_id: str, client_secret: str) -> str:
        pass
