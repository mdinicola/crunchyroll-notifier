from services.crunchyroll import CrunchyList, CrunchyItem
from services.db import SeriesTable
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, crunchyroll_service = None, db_connection = None):
        self.crunchyroll_service = crunchyroll_service
        self.db_connection = db_connection

    def sync_list(self, crunchy_list: CrunchyList):
        items = crunchy_list.items
        series = filter(lambda i: i.type == "series", items)
        for show in series:
            self.sync_series(show)

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

    def sync_seasons(self):
        pass

    def sync_episodes(self):
        pass