from services.aws_secrets_manager import SecretsManagerService, SecretsManagerSecret
import os
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

_APP_SECRET_NAME_KEY = 'SecretName'

class ConfigService:
    _secrets_manager_service = SecretsManagerService()

    def __init__(self, crunchyroll_config: dict, filters: dict, pushover_config: dict, db_config: dict):
            self.crunchyroll = crunchyroll_config
            self.filters = filters
            self.pushover = pushover_config
            self.db = db_config

    @classmethod
    def load_config(cls):
        app_secret_name = os.environ[_APP_SECRET_NAME_KEY]
        app_secret: SecretsManagerSecret = ConfigService._secrets_manager_service.get_secret(app_secret_name)

        crunchyroll_config = {
            'email': app_secret.get_value('CrunchyrollEmail'),
            'password': app_secret.get_value('CrunchyrollPassword')
        }
        
        filters = {
            'list_id': app_secret.get_value('CrunchyrollFiltersListId'),
            'is_dubbed': app_secret.get_value('CrunchyrollFiltersIsDubbed'),
            'time_period_in_days': app_secret.get_value('CrunchyrollFiltersTimePeriodInDays'),
            'audio_locales': list(filter(None, app_secret.get_value('CrunchyrollFiltersAudioLocales', '').split(','))),
            'subtitle_locales': list(filter(None, app_secret.get_value('CrunchyrollFiltersSubtitleLocales', '').split(','))),
        }
        
        pushover_config = {
            'user_token': app_secret.get_value('PushoverUserToken'),
            'app_token': app_secret.get_value('PushoverAppToken')
        }
        
        db_config = {
            'host': app_secret.get_value('DbHost'),
            'port': app_secret.get_value('DbPort'),
            'user': app_secret.get_value('DbUser'),
            'password': app_secret.get_value('DbPassword'),
            'db_name': app_secret.get_value('DbName')
        }
        
        return cls(crunchyroll_config, filters, pushover_config, db_config)