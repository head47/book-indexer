from peewee import Database

from src.db_models import Metadata as MetadataModel
from src.db_models import database


def from_config(config: dict) -> Database:
    database.init(
        config["database"]["db"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        host=config["database"]["host"],
        port=config["database"].get("port", 5432),
    )
    database.connect()
    database.create_tables((MetadataModel,))

    return database
