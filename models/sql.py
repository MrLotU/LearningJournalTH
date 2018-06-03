from peewee import SqliteDatabase, Model

db = SqliteDatabase('journal.sqlite')

MODELS = []

class BaseModel(Model):
    """Database Base Model class"""
    class Meta:
        # Set database
        database = db

    @staticmethod
    def register(cls):
        """Registers new model to the DB"""
        MODELS.append(cls)
        return cls

def init_db():
    """Sets up DB for use"""
    for model in MODELS:
        model.create_table(True)
