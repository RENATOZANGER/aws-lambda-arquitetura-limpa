import json
import os
import boto3
import pytest
from src.utils.exceptions import GetSecretError
from tests.fixtures import mock_env_vars
from moto import mock_aws

class TestSecretsAws:
    @mock_aws
    def test_get_secrets_success_com_json(self,mock_env_vars):
        from src.use_cases.get_secrets_manager_use_case import GetSecretsManagerUseCase
        from src.adapters.secrets_manager_adapter import SecretsManagerAdapter
        conn = boto3.client("secretsmanager", region_name='sa-east-1')
        secret_string = json.dumps({
            'client_id': 'mock_id',
            'client_secret': 'mock_secret'
        })
        conn.create_secret(Name=os.environ.get('ARN_CLIENT_ID_CLIENT_SECRET'), SecretString=secret_string)
        
        use_case = GetSecretsManagerUseCase(aws_secret_adapter=SecretsManagerAdapter())
        retorno = use_case.get_secrets(
            secret_id=os.environ.get('ARN_CLIENT_ID_CLIENT_SECRET')
        )
        assert retorno["client_id"] == 'mock_id'
    
    @mock_aws
    def test_get_secrets_success_sem_json(self, mock_env_vars):
        from src.use_cases.get_secrets_manager_use_case import GetSecretsManagerUseCase
        from src.adapters.secrets_manager_adapter import SecretsManagerAdapter
        conn = boto3.client("secretsmanager", region_name='sa-east-1')
        secret_string = 'mock'
        conn.create_secret(Name=os.environ.get('ARN_CLIENT_ID_CLIENT_SECRET'), SecretString=secret_string)
        
        use_case = GetSecretsManagerUseCase(aws_secret_adapter=SecretsManagerAdapter())
        retorno = use_case.get_secrets(
            secret_id=os.environ.get('ARN_CLIENT_ID_CLIENT_SECRET')
        )
        assert retorno == 'mock'
        
    def test_get_secrets_failure(self, mock_env_vars):
        from src.use_cases.get_secrets_manager_use_case import GetSecretsManagerUseCase
        from src.adapters.secrets_manager_adapter import SecretsManagerAdapter
        use_case = GetSecretsManagerUseCase(aws_secret_adapter=SecretsManagerAdapter())
        with pytest.raises(GetSecretError):
            use_case.get_secrets(
                secret_id='arn:aws:secretsmanager:sa-east-1:123456789012:secret:test'
            )
