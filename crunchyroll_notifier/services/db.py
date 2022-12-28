from peewee import *
import logging

_logger = logging.getLogger(__name__)
_database = MySQLDatabase(None)

class DatabaseService:
    def __init__(self):
        self.db_connection = _database
    
    def init_connection(self, host: str, port: int, user: str, password: str, db_name: str):
        self.db_connection.autoconnect = False
        self.db_connection.init(db_name, host = host, port = int(port), charset = 'utf8', sql_mode = 'PIPES_AS_CONCAT', 
            use_unicode = True, user = user, password = password)
        return self.db_connection

class BaseModel(Model):
    class Meta:
        database = _database

class SeriesTable(BaseModel):
    date_added = DateTimeField()
    id = CharField(primary_key=True)
    slug_title = CharField()
    title = CharField()

    class Meta:
        table_name = 'series'

class SeasonsTable(BaseModel):
    date_added = DateTimeField()
    id = CharField(primary_key=True)
    series = ForeignKeyField(column_name='series_id', field='id', model=SeriesTable)
    slug_title = CharField()
    title = CharField()

    class Meta:
        table_name = 'seasons'

class EpisodesTable(BaseModel):
    date_added = DateTimeField()
    id = CharField(primary_key=True)
    is_dubbed = IntegerField()
    is_subbed = IntegerField()
    season = ForeignKeyField(column_name='season_id', field='id', model=SeasonsTable)
    series = ForeignKeyField(column_name='series_id', field='id', model=SeriesTable)
    slug_title = CharField()
    title = CharField()

    class Meta:
        table_name = 'episodes'

class LocalesTable(BaseModel):
    audio_locale = CharField()
    episode = ForeignKeyField(column_name='episode_id', field='id', model=EpisodesTable)
    subtitle_locale = CharField()

    class Meta:
        table_name = 'locales'