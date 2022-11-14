from crunchyroll_beta import Crunchyroll
from datetime import datetime, timezone
from dateutil import parser
import logging

_logger = logging.getLogger(__name__)

class CrunchyrollClient:
    def __init__(self, email: str, password: str):
        self._cr = Crunchyroll(email, password)

    def start_session(self):
        self._cr.start()

    def get_custom_list(self, list_id):
        return self._cr.get_custom_list(list_id)