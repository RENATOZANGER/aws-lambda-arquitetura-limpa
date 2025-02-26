# aws-lambda-arquitetura-limpa
 Exemplo de aplicação em python usando Arquitetura Limpa no lambda na aws

## Aplicação

Essa aplicação consiste em:
- Consultar uma tabela e verificar quais registros possui o status Cancelado
- Chamar uma api passando os registros para obter as informações de alguns campos
- Após o retorno da api, atualizar a tabela com o retorno dos campos da api
- Caso a api, nao retorne nenhum valor, processar o proximo registro
