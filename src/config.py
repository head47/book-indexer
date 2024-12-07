from dataclasses import dataclass

from alt_utils import NestedDeserializableDataclass


@dataclass
class DatabaseConfig:
    db: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class Config(NestedDeserializableDataclass):
    database: DatabaseConfig
