from unittest.mock import Mock, MagicMock, patch
from typing import Dict
import handlers.api_handler as api_handler
import json
import logging

_logger = logging.getLogger(__name__)

@patch('handlers.api_handler.CrunchyrollClient.start_session')
@patch('services.crunchyroll.Crunchyroll._make_request')
def get_crunchylists(event, context, mock_request, mock_session):
    mock_session.return_value = Mock()

    with open('test/custom_lists.json', 'r') as f:
        data = json.load(f)
    
    mock_request.return_value = data

    return api_handler.get_crunchylists(event, context)

@patch('handlers.api_handler.CrunchyrollClient.start_session')
@patch('services.crunchyroll.Crunchyroll._make_request')
def get_crunchylist(event, context, mock_request, mock_session):
    mock_session.return_value = Mock()

    with open('test/custom_list.json', 'r') as f:
        data = json.load(f)
    m = MagicMock()
    m.__getitem__.side_effect = data.__getitem__
    mock_request.return_value = m
    return api_handler.get_crunchylist(event, context)