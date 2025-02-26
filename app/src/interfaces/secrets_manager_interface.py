from abc import abstractmethod, ABC
from typing import Union, Dict, Any


class SecretsManagerInterface(ABC):
    @abstractmethod
    def get_secrets(self, secret_id: str) -> Union[Dict[str, Any],str]:
        pass
