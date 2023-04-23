from common.enhanced_json_encoder import EnhancedJSONEncoder
from services.config import ConfigService
from services.crunchyroll import CrunchyrollService
from services.notifications import NotificationService
from os import environ
import json
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_config = ConfigService.load_config()
_crunchyroll_service = CrunchyrollService(_config.crunchyroll)

def handle_response(status_code, body):
    return {
            'statusCode': status_code,
            'body': body
        }

def handle_filters(parameters, filter_keys):
    filters = _config.filters
    for filter_key in filter_keys:
        if parameters is not None and parameters.get(filter_key) is not None:
            filters[filter_key] = parameters.get(filter_key)
        
    return filters

def get_crunchylists(event, context):
    try:
        crunchy_lists = _crunchyroll_service.get_custom_lists()
        response = {
            'total': len(crunchy_lists),
            'data': crunchy_lists
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))

def get_crunchylist(event, context):
    try:
        crunchy_list = _crunchyroll_service.get_custom_list(event['pathParameters']['id'])
        return handle_response(200, json.dumps(crunchy_list, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))

def get_recently_added_episodes(event, context):
    try:
        query_parameters = event.get('queryStringParameters', {})
        
        filter_keys = [ 'time_period_in_days', 'list_id', 'audio_locales', 'is_dubbed' ]
        filters = handle_filters(query_parameters, filter_keys)
        
        recently_added_episodes = _crunchyroll_service.get_recently_added_episodes_from_list(filters['list_id'], filters)
        
        response = {
            'meta': { 'filters': filters, 'count': len(recently_added_episodes) },
            'data': recently_added_episodes
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))
    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))

def get_recently_added_episode_notifications(event, context):
    try:
        query_parameters = event.get('queryStringParameters', {})
        
        filter_keys = [ 'time_period_in_days', 'list_id', 'audio_locales', 'is_dubbed' ]
        filters = handle_filters(query_parameters, filter_keys)
        
        recently_added_episodes = _crunchyroll_service.get_recently_added_episodes_from_list(filters['list_id'], filters)
        notifications = NotificationService.get_notifications("New Anime Released", 
            recently_added_episodes, environ['NotificationSound'])
        
        response = {
            'meta': { 'filters': filters, 'count': len(recently_added_episodes) },
            'data': notifications
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))

    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))
        
def notify_on_recently_added_episodes(event, context):
    try:
        query_parameters = event.get('queryStringParameters', {})
        filter_keys = [ 'time_period_in_days', 'list_id', 'audio_locales', 'is_dubbed' ]
        filters = handle_filters(query_parameters, filter_keys)
        
        recently_added_episodes = _crunchyroll_service.get_recently_added_episodes_from_list(filters['list_id'], filters)
        notifications = NotificationService.get_notifications("New Anime Released", 
            recently_added_episodes, environ['NotificationSound'])
        
        notification_service = NotificationService()
        notification_service.configure_pushover_client(_config.pushover)
        
        response = {
            'meta': { 'filters': filters, 'count': len(recently_added_episodes) },
            'data': [notification_service.notify(notification) for notification in notifications]
        }
        return handle_response(200, json.dumps(response, cls=EnhancedJSONEncoder))

    except Exception as e:
        _logger.exception(e)
        message = 'An unexpected error ocurred.  See log for details.'
        response = {
            'error': {
                'message': message
            }
        }
        return handle_response(500, json.dumps(response))
