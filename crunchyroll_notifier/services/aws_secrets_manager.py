from os import environ
import json
import logging
import boto3

_logger = logging.getLogger(__name__)

class SecretsManagerSecret:

    @staticmethod
    def get_client():
        secretsManagerEndpoint = environ.get('SecretsManagerEndpoint')
        if secretsManagerEndpoint != '':
            return boto3.client('secretsmanager', endpoint_url = secretsManagerEndpoint)
        return boto3.client('secretsmanager')

    def __init__(self, client, secret_name):
        self._client = client
        self.secret_name = secret_name
        self._secret = None

    def _get_secret(self):
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

    def get_value(self, key):
        if self._secret is None:
            self._get_secret()
        
        return self._secret.get(key)

