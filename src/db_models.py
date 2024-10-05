from peewee import CharField, Model, PostgresqlDatabase

database = PostgresqlDatabase(None)


class ModelWithDb(Model):
    class Meta:
        database = database


class Metadata(ModelWithDb):
    title = CharField(index=True)
    author_list = CharField(index=True)
    series = CharField(null=True, index=True)
    lang = CharField()
    format = CharField()
    virtual_filename = CharField(unique=True)
