from peewee import Database

from .config import Config
from .db_models import Metadata as MetadataModel
from .db_models import database


def from_config(config: Config) -> Database:
    database.init(
        config.database.db,
        user=config.database.user,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port,
    )
    database.connect()
    database.create_tables((MetadataModel,))

    return database
