from services.aws_secrets_manager import SecretsManagerSecret
from os import environ
import logging

_logger = logging.getLogger(__name__)

class ConfigService:
    _secrets_manager_client = SecretsManagerSecret.get_client()

    def __init__(self, email: str, password: str, list_id: str, time_period_in_days: int):
        self.email = email
        self.password = password
        self.list_id = list_id
        self.time_period_in_days = time_period_in_days

    @classmethod
    def load_config(cls, secret_name: str):
        secret = SecretsManagerSecret(ConfigService._secrets_manager_client, secret_name)
        return cls(email = secret.get_value('CrunchyrollEmail'), 
            password = secret.get_value('CrunchyrollPassword'), 
            list_id = secret.get_value('CrunchyrollListId'),
            time_period_in_days = secret.get_value('CrunchyrollTimePeriodInDays'))