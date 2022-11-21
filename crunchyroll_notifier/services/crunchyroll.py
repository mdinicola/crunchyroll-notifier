from crunchyroll_beta import Crunchyroll
from datetime import datetime, timezone
from dateutil import parser
from typing import List
import logging

_logger = logging.getLogger(__name__)

class CrunchyrollService:
    _default_filters = {
            'sort_by': "newly_added",
            'max_results': 10,
            'start_value': 0,
            'is_dubbed': None,
            'is_subbed': None,
            'time_period_in_days': None,
            'list_id': None
        }

    def __init__(self, email: str, password: str):
        self._crunchyroll_client = Crunchyroll(email, password)

    def start_session(self):
        self._crunchyroll_client.start()

    def get_custom_lists(self):
        lists = self._crunchyroll_client.get_custom_lists()
        return [CrunchyList(item.list_id, item) for item in lists]

    def get_custom_list(self, list_id):
        list = self._crunchyroll_client.get_custom_list(list_id)
        return CrunchyList(list_id, list)

    def get_recently_added(self, filters):
        filters = CrunchyrollService._default_filters | filters
       
        items = self._crunchyroll_client.browse(sort_by=filters['sort_by'], max_results=filters['max_results'], 
            start_value=filters['start_value'], is_subbed=filters['is_subbed'], is_dubbed=filters['is_dubbed'])
        crunchy_items = []

        time_period_in_days = filters.get('time_period_in_days')
        if time_period_in_days is not None:
            current_time = datetime.now(timezone.utc)
            for item in items:
                last_public = parser.parse(item.last_public)
                if (current_time - last_public).days < int(time_period_in_days):
                    crunchy_items.append(CrunchyItem(item))
        else:
            crunchy_items = [CrunchyItem(item) for item in items]
        
        return crunchy_items

    def get_recently_added_notifications(self, filters):
        filters = CrunchyrollService._default_filters | filters
        recently_added_items = self.get_recently_added(filters)
        list_id = filters.get('list_id')
        if list_id is not None:
            list_items = self.get_custom_list(list_id).items
            items = list(set(recently_added_items).intersection(set(list_items)))
        else:
            items = recently_added_items
        notifications = [CrunchyNotification(f"New anime released: {item.title}") for item in items]
        return notifications


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

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

class CrunchyItem:
    def __init__(self, data):
        self.id: str = data.id
        self.type: str = data.type
        self.title: str = data.title
        self.slug_title: str = data.slug_title
        self.description: str = data.description
        self.is_dubbed: bool = data.series_metadata.is_dubbed
        self.is_subbed: bool = data.series_metadata.is_subbed
        self.last_public: str = data.last_public

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

class CrunchyNotification:
    def __init__(self, message):
        self.message = message