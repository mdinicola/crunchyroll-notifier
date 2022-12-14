from crunchyroll_beta import Crunchyroll
from datetime import datetime, timezone
from dateutil import parser
from typing import List
import logging

_logger = logging.getLogger(__name__)

class CrunchyrollService:
    _default_filters = {
            'max_results': 10,
            'start_value': 0,
            'is_dubbed': None,
            'is_subbed': None,
            'time_period_in_days': 7,
            'list_id': None
        }

    def __init__(self, email: str, password: str):
        self._crunchyroll_client = Crunchyroll(email, password)

    def start_session(self):
        self._crunchyroll_client.start()

    def get_custom_lists(self):
        lists = self._crunchyroll_client.get_custom_lists()
        return [CrunchyList(item.list_id, item) for item in lists]

    def get_custom_list(self, list_id: str):
        list = self._crunchyroll_client.get_custom_list(list_id)
        return CrunchyList(list_id, list)

    def get_seasons(self, series_id: str):
        items = self._crunchyroll_client.get_seasons(series_id)
        return [CrunchySeason(item) for item in items]

    def get_episodes(self, season_id: str):
        items = self._crunchyroll_client.get_episodes(season_id)
        return [CrunchyEpisode(item) for item in items]

    def get_recently_added_episodes_from_list(self, list_id: str, filters: dict):
        items = []
        time_period_in_days = filters.get('time_period_in_days')
        current_time = datetime.now(timezone.utc)
        for series in self.get_custom_list(list_id).items:
            for season in self.get_seasons(series.id):
                if (len(filters['audio_locales']) == 0 or (season.audio_locale in filters['audio_locales'] and 
                    (filters['is_dubbed'] is not None and season.is_dubbed == bool(filters['is_dubbed'])))):
                    for episode in self.get_episodes(season.id):
                        if (current_time - parser.parse(episode.upload_date)).days < int(time_period_in_days):
                            if (filters['is_dubbed'] is not None and episode.is_dubbed == bool(filters['is_dubbed'])):
                                items.append(episode)
        return items             

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

class CrunchySeason:
    def __init__(self, data):
        self.id: str = data.id
        self.title: str = data.title
        self.slug_title: str = data.slug_title
        self.series_id: str = data.series_id
        self.season_number: int = data.season_number
        self.is_subbed: bool = data.is_subbed
        self.is_dubbed: bool = data.is_dubbed
        self.audio_locale: str = data.audio_locale
        self.audio_locales: List[str] = data.audio_locales
        self.subtitle_locales: List[str] = data.subtitle_locales

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

class CrunchyEpisode:
    def __init__(self, data: dict):
        self.id: str = data.id
        self.series_id: str = data.series_id
        self.series_title: str = data.series_title
        self.season_id: str = data.season_id
        self.season_title: str = data.season_title
        self.season_number: int = data.season_number
        self.episode: str = data.episode
        self.episode_number: int = data.episode_number
        self.title: str = data.title
        self.slug_title: str = data.slug_title
        self.is_subbed: bool = data.is_subbed
        self.is_dubbed: bool = data.is_dubbed
        self.audio_locale: str = data.audio_locale
        self.subtitle_locales: List[str] = data.subtitle_locales
        self.upload_date: str = data.upload_date
        
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)