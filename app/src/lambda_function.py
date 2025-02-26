import json
from src.adapters.api_conta_adapter import ApiContaAdapter
from src.adapters.database_adapter import DataBaseAdapter
from src.adapters.processa_contratos_adapter import ProcessaContratosAdapter
from src.adapters.secrets_manager_adapter import SecretsManagerAdapter
from src.infra.db_connection import DBConnection
from src.use_cases.get_secrets_manager_use_case import GetSecretsManagerUseCase
from src.use_cases.processa_contrato_use_case import ProcessaContratoUseCase
from src.utils import LOGGER
from src.utils.enums import Credenciais


def lambda_handler(event, context):
    try:
        LOGGER.info(
            log_code="lambda_handler",
            log_message="Iniciando o proceso",
            payload=event
        )
        
        secrets_manager_adapter = SecretsManagerAdapter()
        get_secret_manager_use_case = GetSecretsManagerUseCase(secrets_manager_adapter)
        client_id_client_secret = get_secret_manager_use_case.get_secrets(
            Credenciais.ARN_CLIENT_ID_CLIENT_SECRET.value
        )
        db_connection = DBConnection(get_secret_manager_use_case)
        database_adapter = DataBaseAdapter(db_connection)
        
        api_conta_adapter = ApiContaAdapter(client_id_client_secret=client_id_client_secret)
        
        processa_contratos_adapter = ProcessaContratosAdapter(
            api_conta_adapter=api_conta_adapter, database_adapter=database_adapter
        )
        
        processa_contrato_use_case = ProcessaContratoUseCase(processa_contratos_adapter)
        
        with database_adapter.conexao:
            processa_contrato_use_case.processa_contrato()
            
        return {
            'statusCode': 200,
            'body': json.dumps({'Sucesso': 'Processamento executado com sucesso'})
        }
    
    except Exception as e:
        LOGGER.error(
            log_code="lambda_handler",
            log_message="Erro ao executar o lambda",
            payload=str(e)
        )
        raise e
