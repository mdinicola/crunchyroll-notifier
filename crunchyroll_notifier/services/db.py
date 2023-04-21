from peewee import *
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_database = MySQLDatabase(None)

class DatabaseService:
    def __init__(self, config: dict):
        self.db_connection = _database
        self.db_connection.autoconnect = False
        self.db_connection.init(database = config.get('db_name'), host = config.get('host'), port = int(config.get('port')), charset = 'utf8', sql_mode = 'PIPES_AS_CONCAT', 
            use_unicode = True, user = config.get('user'), password = config.get('password'))

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