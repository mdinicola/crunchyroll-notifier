from common.enhanced_json_encoder import EnhancedJSONEncoder
from services.config import ConfigService
from services.crunchyroll import CrunchyrollService
from os import environ
import json
import logging

_logger = logging.getLogger(__name__)
_config = ConfigService.load_config(environ['SecretName'])

def _get_crunchyroll_service():
    try:
        crunchyroll_service = CrunchyrollService(email = _config.crunchyroll_credentials.get('email'), 
            password = _config.crunchyroll_credentials.get('password'))
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
        if parameters is not None and parameters.get(filter_key) is not None:
            filters[filter_key] = parameters.get(filter_key)
        elif _config.crunchyroll_filters.get(filter_key) is not None:
            filters[filter_key] = _config.crunchyroll_filters.get(filter_key)
        
    return filters

def get_crunchylists(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service()
        crunchy_lists = crunchyroll_service.get_custom_lists()
        response = {
            'total': len(crunchy_lists),
            'data': crunchy_lists
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))
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
        filter_keys = [ 'sort_by', 'max_results', 'start_value', 'is_dubbed', 'is_subbed', 'time_period_in_days', 'list_id' ]
        filters = handle_filters(query_parameters, filter_keys)
        recently_added = crunchyroll_service.get_recently_added(filters)
        response = {
            'filters': filters,
            'total': len(recently_added),
            'data': recently_added
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))

def get_recently_added_notifications(event, context):
    try:
        crunchyroll_service = _get_crunchyroll_service(_config.email, _config.password)
        query_parameters = event['queryStringParameters']
        filter_keys = [ 'sort_by', 'max_results', 'start_value', 'is_dubbed', 'is_subbed', 'time_period_in_days', 'list_id' ]
        filters = handle_filters(query_parameters, filter_keys)
        notifications = crunchyroll_service.get_recently_added_notifications(filters)
        response = {
            'filters': filters,
            'total': len(notifications),
            'data': notifications
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))

    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        return handle_response(500, json.dumps({'message': message}))
        
