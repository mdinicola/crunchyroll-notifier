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

    def get_custom_list(self, list_id):
        list = self._cr.get_custom_list(list_id)
        return CrunchyList(list_id, list)

class CrunchyList:
    def __init__(self, list_id, data: dict):
        self.id = list_id
        self.title: str = data.get("title")
        self.total: int = data.get("total")
        self.is_public: bool = data.get("is_public")
        self.modified_at: str = data.get("modified_at")
        self.items: List[CrunchyListItem] = [CrunchyListItem(item) for item in data.get("items", [])]

class CrunchyListItem:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: str = data.get("panel").get("type")
        self.title: str = data.get("panel").get("title")
        self.slug_title: str = data.get("panel").get("slug_title")
        self.description: str = data.get("panel").get("description")
        self.is_dubbed: bool = data.get("panel").get("series_metadata").get("is_dubbed")
        self.is_subbed: bool = data.get("panel").get("series_metadata").get("is_subbed")