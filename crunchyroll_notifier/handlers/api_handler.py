from common.enhanced_json_encoder import EnhancedJSONEncoder
from services.aws_secrets_manager import SecretsManagerSecret
from services.crunchyroll import CrunchyrollClient
from os import environ
import json
import logging

_logger = logging.getLogger(__name__)
_secrets_manager_client = SecretsManagerSecret.get_client()

AWS_SECRET_NAME = environ['SecretName']
CRUNCHYROLL_EMAIL_KEY = 'CrunchyrollEmail'
CRUNCHYROLL_PASSWORD_KEY = 'CrunchyrollPassword'
CRUNCHYROLL_LIST_ID_KEY = 'CrunchyrollListId'

def _get_config():
    secret = SecretsManagerSecret(_secrets_manager_client, secret_name = AWS_SECRET_NAME)
    email = secret.get_value(CRUNCHYROLL_EMAIL_KEY)
    password = secret.get_value(CRUNCHYROLL_PASSWORD_KEY)
    list_id = secret.get_value(CRUNCHYROLL_LIST_ID_KEY)
    if email == '' or password == '' or list_id == '':
        return None
    return { CRUNCHYROLL_EMAIL_KEY: email, CRUNCHYROLL_PASSWORD_KEY: password, CRUNCHYROLL_LIST_ID_KEY: list_id }

def get_crunchylists(event, context):
    try:
        config = _get_config()
        crunchyroll_client = CrunchyrollClient(config[CRUNCHYROLL_EMAIL_KEY], config[CRUNCHYROLL_PASSWORD_KEY])
        crunchyroll_client.start_session()
        crunchy_lists = crunchyroll_client.get_custom_lists()

        return {
            'statusCode': 200,
            'body': json.dumps(crunchy_lists, cls=EnhancedJSONEncoder)
        }
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return {
            'statusCode': 500,
            'body': json.dumps({'message': message})
        }

def get_crunchylist(event, context):
    try:
        config = _get_config()
        crunchyroll_client = CrunchyrollClient(config[CRUNCHYROLL_EMAIL_KEY], config[CRUNCHYROLL_PASSWORD_KEY])
        crunchyroll_client.start_session()
        crunchy_list = crunchyroll_client.get_custom_list(event['pathParameters']['id'])

        return {
            'statusCode': 200,
            'body': json.dumps(crunchy_list, cls=EnhancedJSONEncoder)
        }
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return {
            'statusCode': 500,
            'body': json.dumps({'message': message})
        }
        
