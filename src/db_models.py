from peewee import CharField, Model, PostgresqlDatabase, TextField

database = PostgresqlDatabase(None)


class ModelWithDb(Model):
    class Meta:
        database = database


class Metadata(ModelWithDb):
    title = TextField(index=True)
    author_list = TextField(index=True)
    translator_list = TextField(index=True)
    series = TextField(index=True)
    lang = CharField()
    format = CharField()
    virtual_filename = TextField(unique=True)

    class Meta:
        indexes = ((("title", "author_list", "translator_list", "series", "lang", "format"), True),)
