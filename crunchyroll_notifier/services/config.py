from services.aws_secrets_manager import SecretsManagerSecret
from os import environ
import logging

_logger = logging.getLogger(__name__)

class ConfigService:
    _secrets_manager_client = SecretsManagerSecret.get_client()

    def __init__(self, crunchyroll_credentials: dict, crunchyroll_filters: dict, 
        pushover_credentials: dict):
            self.crunchyroll_credentials = crunchyroll_credentials
            self.crunchyroll_filters = crunchyroll_filters


    @classmethod
    def load_config(cls, secret_name: str):
        secret = SecretsManagerSecret(ConfigService._secrets_manager_client, secret_name)
        crunchyroll_credentials = {
            'email': secret.get_value('CrunchyrollEmail'),
            'password': secret.get_value('CrunchyrollPassword')
        }
        crunchyroll_filters = {
            'list_id': secret.get_value('CrunchyrollFiltersListId'),
            'time_period_in_days': secret.get_value('CrunchyrollFiltersTimePeriodInDays')
        }

        return cls(crunchyroll_credentials = crunchyroll_credentials, 
            crunchyroll_filters = crunchyroll_filters)