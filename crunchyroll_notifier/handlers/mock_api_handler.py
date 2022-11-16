from unittest.mock import Mock, patch
import handlers.api_handler as api_handler
import json
import logging

_logger = logging.getLogger(__name__)

@patch('handlers.api_handler.CrunchyrollClient.start_session', autospec=True)
@patch('services.crunchyroll.Crunchyroll.get_custom_list', autospec=True)
def get_crunchylist(event, context, mock_list, mock_session):
    mock_session.return_value = Mock()

    with open('test/custom_list.json', 'r') as f:
        data = json.load(f)
    
    mock_list.return_value = data

    return api_handler.get_crunchylist(event, context)