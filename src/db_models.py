from peewee import CharField, Model, PostgresqlDatabase

database = PostgresqlDatabase(None)


class ModelWithDb(Model):
    class Meta:
        database = database


class Metadata(ModelWithDb):
    title = CharField(index=True)
    author_list = CharField(index=True)
    translator_list = CharField(index=True)
    series = CharField(index=True)
    lang = CharField()
    format = CharField()
    virtual_filename = CharField(unique=True)

    class Meta:
        indexes = ((("title", "author_list", "translator_list", "series", "lang", "format"), True),)
