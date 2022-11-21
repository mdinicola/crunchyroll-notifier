from common.enhanced_json_encoder import EnhancedJSONEncoder
from services.aws_secrets_manager import SecretsManagerSecret
from services.crunchyroll import CrunchyrollService
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

def _get_crunchyroll_service():
    try:
        config = _get_config()
        crunchyroll_service = CrunchyrollService(config[CRUNCHYROLL_EMAIL_KEY], config[CRUNCHYROLL_PASSWORD_KEY])
        crunchyroll_service.start_session()
        return crunchyroll_service
    except Exception as e:
        _logger.exception(f"An error occurred while getting the client: {e}")
        raise

def handle_response(status_code, body):
    return {
            'statusCode': status_code,
            'body': body
        }

def handle_filters(parameters, filter_keys):
    filters = {}
    for filter_key in filter_keys:
        if parameters.get(filter_key) is not None:
            filters[filter_key] = parameters.get(filter_key)
    return filters

def get_crunchylists(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service()
        crunchy_lists = crunchyroll_service.get_custom_lists()
        return handle_response(200, json.dumps(crunchy_lists, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_crunchylist(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service()
        crunchy_list = crunchyroll_service.get_custom_list(event['pathParameters']['id'])
        return handle_response(200, json.dumps(crunchy_list, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_recently_added(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service()
        query_parameters = event['queryStringParameters']
        filter_keys = [ 'sort_by', 'max_results', 'start_value', 'is_dubbed', 'is_subbed', 'time_period_in_days' ]
        filters = handle_filters(query_parameters, filter_keys) if query_parameters is not None else {}
        recently_added = crunchyroll_service.get_recently_added(filters)
        return handle_response(200, json.dumps(recently_added, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_recently_added_notifications(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service()
        query_parameters = event['queryStringParameters']
        filter_keys = [ 'sort_by', 'max_results', 'start_value', 'is_dubbed', 'is_subbed', 'time_period_in_days', 'list_id' ]
        filters = handle_filters(query_parameters, filter_keys) if query_parameters is not None else {}
        notifications = crunchyroll_service.get_recently_added_notifications(filters)
        return handle_response(200, json.dumps(notifications, cls=EnhancedJSONEncoder))

    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))
        
