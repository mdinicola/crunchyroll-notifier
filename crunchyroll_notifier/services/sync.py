from services.crunchyroll import CrunchyrollService, CrunchyList, CrunchyItem
from services.db import SeriesTable, SeasonsTable
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, filters, crunchyroll_service: CrunchyrollService = None, db_connection = None):
        self.filters = filters
        self.crunchyroll_service = crunchyroll_service
        self.db_connection = db_connection

    def sync_list(self, crunchy_list: CrunchyList):
        items = crunchy_list.items
        series = filter(lambda i: i.type == "series", items)
        for show in series:
            self.sync_series(show)
            self.sync_seasons(show)

    def sync_series(self, series: CrunchyItem):
        series_table = SeriesTable()
        series_table.id = series.id
        series_table.title = series.title
        series_table.slug_title = series.slug_title
        series_table.date_added = datetime.now()
        with self.db_connection:
            series = SeriesTable.get_or_none(SeriesTable.id == series.id)
            if series is None:
                series_table.save(force_insert = True)

    def sync_seasons(self, series: CrunchyItem):
        seasons = self.crunchyroll_service.get_seasons(series.id)
        for season in seasons:
            if (len(self.filters['audio_locales']) == 0 or len(self.filters['subtitle_locales']) == 0
                or season.audio_locale in self.filters['audio_locales']
                or any(item in season.subtitle_locales for item in self.filters['subtitle_locales'])):
                    seasons_table = SeasonsTable()
                    seasons_table.id = season.id
                    seasons_table.title = season.title
                    seasons_table.slug_title = season.slug_title
                    seasons_table.date_added = datetime.now()
                    with self.db_connection:
                        seasons_table.series = SeriesTable.get(SeriesTable.id == series.id)
                        db_season = SeasonsTable.get_or_none(SeasonsTable.id == seasons_table.id)
                        if db_season is None:
                            seasons_table.save(force_insert = True)

    def sync_episodes(self):
        pass