import os
import json
import logging
import boto3

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

class SecretsManagerSecret:
    def __init__(self, client, secret_name) -> None:
        self._client = client
        self.secret_name = secret_name
        self._secret = None

    def _get_secret(self) -> None:
        if self.secret_name is None:
            raise ValueError

        try:
            data = { 'SecretId': self.secret_name }
            response = self._client.get_secret_value(**data)
            if 'SecretString' in response:
                self._secret = json.loads(response.get('SecretString'))
            else:
                _logger.exception(f'Missing SecretString in secret {self.secret_name}')
                raise KeyError
        except Exception as e:
            _logger.exception(f'Could not get secret value for {self.secret_name} with error {e}')
            raise

    def get_value(self, key, default_value = None):
        if self._secret is None:
            self._get_secret()
        
        return self._secret.get(key, default_value)

    def put_values(self, **kwargs) -> None:
        if self._secret is None:
            self._get_secret()
        try:
            for key, value in kwargs.items():
                self._secret[key] = value
            data = { 'SecretId': self.secret_name, 'SecretString': json.dumps(self._secret) }
            response = self._client.put_secret_value(**data)
            _logger.info(f'Successfully updated secret {response["Name"]}.  New version id is {response["VersionId"]}')
        except Exception as e:
            _logger.exception(f'Could not get secret value for {self.secret_name} with error {e}')
            raise

class SecretsManagerService:

    @staticmethod
    def get_client():
        secretsManagerEndpoint = os.environ.get('SecretsManagerEndpoint')
        if secretsManagerEndpoint != '':
            return boto3.client('secretsmanager', endpoint_url = secretsManagerEndpoint)
        return boto3.client('secretsmanager')

    def __init__(self, client = None) -> None:
        self.client = client
        if self.client is None:
            self.client = SecretsManagerService.get_client()
        self.secrets_manager_endpoint = os.environ.get('SecretsManagerEndpoint')
        self._secret = None

    def set_client(self, client) -> None:
        self.client = client

    def get_secret(self, secret_name) -> SecretsManagerSecret:
        return SecretsManagerSecret(self.client, secret_name)

