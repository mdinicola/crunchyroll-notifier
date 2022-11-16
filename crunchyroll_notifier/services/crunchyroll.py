from crunchyroll_beta import Crunchyroll
from datetime import datetime, timezone
from dateutil import parser
from typing import List
import logging

_logger = logging.getLogger(__name__)

class CrunchyrollClient:
    def __init__(self, email: str, password: str):
        self._cr = Crunchyroll(email, password)

    def start_session(self):
        self._cr.start()

    def get_custom_lists(self):
        lists = self._cr.get_custom_lists()
        # return lists
        return [CrunchyList(item.list_id, item) for item in lists]

    def get_custom_list(self, list_id):
        list = self._cr.get_custom_list(list_id)
        # return list
        return CrunchyList(list_id, list)

class CrunchyList:
    def __init__(self, list_id, data):
        self.id = list_id
        self.title: str = data.title
        self.total: int = data.total
        self.is_public: bool = data.is_public
        self.modified_at: str = data.modified_at
        self.items: List[CrunchyListItem] = [CrunchyListItem(item) for item in data.items]

class CrunchyListItem:
    def __init__(self, data):
        self.id: str = data.id
        self.type: str = data.panel.type
        self.title: str = data.panel.title
        self.slug_title: str = data.panel.slug_title
        self.description: str = data.panel.description
        self.is_dubbed: bool = data.panel.series_metadata.is_dubbed
        self.is_subbed: bool = data.panel.series_metadata.is_subbed