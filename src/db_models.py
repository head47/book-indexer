from peewee import CharField, Model, TextField
from playhouse.postgres_ext import PostgresqlExtDatabase, TSVectorField

database = PostgresqlExtDatabase(None)


class ModelWithDb(Model):
    class Meta:
        database = database


class Metadata(ModelWithDb):
    title = TextField()
    title_search = TSVectorField()

    author_list = TextField()
    author_list_search = TSVectorField()

    translator_list = TextField()
    translator_list_search = TSVectorField()

    series = TextField()
    series_search = TSVectorField()

    lang = CharField()
    format = CharField()
    hash = CharField(64, unique=True)
    virtual_filename = TextField(unique=True)
