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

def _get_crunchyroll_client():
    try:
        config = _get_config()
        crunchyroll_client = CrunchyrollClient(config[CRUNCHYROLL_EMAIL_KEY], config[CRUNCHYROLL_PASSWORD_KEY])
        crunchyroll_client.start_session()
        return crunchyroll_client
    except Exception as e:
        _logger.exception(f"An error occurred while getting the client: {e}")
        raise

def handle_response(status_code, body):
    return {
            'statusCode': status_code,
            'body': body
        }

def get_crunchylists(event, context):
    try:
        crunchyroll_client = _get_crunchyroll_client()
        crunchy_lists = crunchyroll_client.get_custom_lists()
        return handle_response(200, json.dumps(crunchy_lists, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_crunchylist(event, context):
    try:
        crunchyroll_client = _get_crunchyroll_client()
        crunchy_list = crunchyroll_client.get_custom_list(event['pathParameters']['id'])
        return handle_response(200, json.dumps(crunchy_list, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_recently_added(event, context):
    try:
        crunchyroll_client = _get_crunchyroll_client()
        options = {}
        query_parameters = event['queryStringParameters']
        if query_parameters is not None:
            if query_parameters.get('is_dubbed') is not None:
                options['is_dubbed'] = bool(query_parameters.get('is_dubbed'))
            if query_parameters.get('is_subbed') is not None:
                options['is_subbed'] = bool(query_parameters.get('is_subbed'))
        
        recently_added = crunchyroll_client.get_recently_added(options)
        return handle_response(200, json.dumps(recently_added, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))
        
