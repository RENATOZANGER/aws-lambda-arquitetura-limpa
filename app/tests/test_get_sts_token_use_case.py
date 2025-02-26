from unittest.mock import MagicMock
import pytest
from src.utils.exceptions import StsError
from tests.fixtures import mock_env_vars, mock_requests

class TestStsToken:
    @pytest.fixture(autouse=True)
    def setup(self, mock_env_vars,mock_requests):
        self.mock_requests = mock_requests
        parameter_store_mock = MagicMock()
        parameter_store_mock.get_values.return_value = "https://mock-sts-url.com"
        
        from src.use_cases.get_sts_token_use_case import GetStsTokenUseCase
        from src.adapters.token_sts_adapter import StsTokenAdapter
        
        self.use_case = GetStsTokenUseCase(token_sts_adapter=StsTokenAdapter())
        
    def test_get_token_sts_success(self):
        self.mock_requests.post(
            "https://mock-sts-url.com",
            json={"access_token": "mock_access_token"},
            status_code = 200
        )
        
        token = self.use_case.get_token_sts("mock_client_id","mock_client_secret")
        assert token == "mock_access_token"
        
    def test_get_token_sts_failure(self):
        self.mock_requests.post(
            "https://mock-sts-url.com",
            json={"error": "invalid_client"},
            status_code=401
        )
        
        parameter_store_mock = MagicMock()
        parameter_store_mock.get_value.return_value = "https://mock-sts-url.com"
        with pytest.raises(StsError):
            self.use_case.get_token_sts("mock_client_id", "mock_client_secret")
