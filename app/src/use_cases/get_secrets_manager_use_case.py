from dataclasses import dataclass
from src.adapters.secrets_manager_adapter import SecretsManagerAdapter


@dataclass
class GetSecretsManagerUseCase:
    aws_secret_adapter: SecretsManagerAdapter
    
    def get_secrets(self, secret_id: str):
        return self.aws_secret_adapter.get_secrets(secret_id)
