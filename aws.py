import boto3
from typing import Union

def get_secret(secret_prefix: str, region_name: str) -> str:
    sm_client = boto3.client('secretsmanager', region_name=region_name)
    response = sm_client.list_secrets()
    secrets = response.get('SecretList', [])
    for secret in secrets:
        if secret_prefix in secret['Name']:
            secret_name = secret['Name']
            break
    else:
        raise Exception("Secret not found or doesn't match the prefix")
    secret_value_response = sm_client.get_secret_value(SecretId=secret_name)
    secret_value = secret_value_response['SecretString']
    return secret_value


def get_ssm_param(parameter_name: Union[str, list], region_name: str) -> dict:
    ssm_client = boto3.client('ssm', region_name=region_name)
    if type(parameter_name) is not list:
        parameter_name = [ parameter_name ]
    response = ssm_client.get_parameters(
        Names=parameter_name,
    )
    return {
        param['Name']: param['Value']
        for param
        in response['Parameters']
    }
