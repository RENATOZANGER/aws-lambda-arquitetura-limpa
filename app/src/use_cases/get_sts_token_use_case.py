from dataclasses import dataclass
from src.adapters.token_sts_adapter import StsTokenAdapter


@dataclass
class GetStsTokenUseCase:
    token_sts_adapter: StsTokenAdapter
    
    def get_token_sts(self, client_id: str, client_secret ):
        return self.token_sts_adapter.get_token_sts(client_id, client_secret)
