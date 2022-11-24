from services.aws_secrets_manager import SecretsManagerSecret
from os import environ
import logging

_logger = logging.getLogger(__name__)

class ConfigService:
    _secrets_manager_client = SecretsManagerSecret.get_client()

    def __init__(self, email: str, password: str, filters: dict):
        self.email = email
        self.password = password
        self.filters = filters

    @classmethod
    def load_config(cls, secret_name: str):
        secret = SecretsManagerSecret(ConfigService._secrets_manager_client, secret_name)
        filters = {
            'list_id': secret.get_value('CrunchyrollFiltersListId'),
            'time_period_in_days': secret.get_value('CrunchyrollFiltersTimePeriodInDays')
        }
        return cls(email = secret.get_value('CrunchyrollEmail'), 
            password = secret.get_value('CrunchyrollPassword'), 
            filters = filters)