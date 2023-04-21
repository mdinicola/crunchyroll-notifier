from services.crunchyroll import CrunchyrollService, CrunchyList, CrunchyItem
from services.db import DatabaseService, SeriesTable, SeasonsTable
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

class SyncService:
    def __init__(self, crunchyroll_service: CrunchyrollService, db_service: DatabaseService):
        self._crunchyroll_service = crunchyroll_service
        self._db_service = db_service

    def sync_list(self, crunchy_list: CrunchyList, filters: dict):
        items = crunchy_list.items
        series = filter(lambda i: i.type == "series", items)
        for show in series:
            self.sync_series(show, filters)
            self.sync_seasons(show, filters)

    def sync_series(self, series: CrunchyItem, filters: dict):
        series_table = SeriesTable()
        series_table.id = series.id
        series_table.title = series.title
        series_table.slug_title = series.slug_title
        series_table.date_added = datetime.now()
        with self._db_service.db_connection:
            series = SeriesTable.get_or_none(SeriesTable.id == series.id)
            if series is None:
                series_table.save(force_insert = True)

    def sync_seasons(self, series: CrunchyItem, filters: dict):
        seasons = self._crunchyroll_service.get_seasons(series.id)
        for season in seasons:
                scan_season = False

                if (len(filters['audio_locales']) == 0 or filters['is_dubbed'] is None):
                    # scan season because filters are not set
                    scan_season = True
                elif (season.is_dubbed == bool(filters['is_dubbed']) and any((True for x in filters['audio_locales'] if x in season.audio_locales))):
                    scan_season = True

                if scan_season:
                    seasons_table = SeasonsTable()
                    seasons_table.id = season.id
                    seasons_table.title = season.title
                    seasons_table.slug_title = season.slug_title
                    seasons_table.date_added = datetime.now()
                    with self._db_service.db_connection:
                        seasons_table.series = SeriesTable.get(SeriesTable.id == series.id)
                        db_season = SeasonsTable.get_or_none(SeasonsTable.id == seasons_table.id)
                        if db_season is None:
                            seasons_table.save(force_insert = True)

    def sync_episodes(self):
        pass