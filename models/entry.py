from peewee import CharField, DateField, TextField
from datetime import datetime
from wtforms import Form, StringField, DateField, validators, ValidationError, widgets
from models import BaseModel

def validate_date(form, field):
    try:
        datetime.strptime(field.data, '%d/%m/%Y')
    except:
        raise ValidationError('Wrong date format. Please use DD/MM/YYYY')

class EntryForm(Form):
    title = StringField('title')
    date = StringField('date', [validate_date])
    time_spent = StringField('time_spent')
    learned = StringField('learned', widget=widgets.TextArea())
    resources = StringField('resources', widget=widgets.TextArea())

@BaseModel.register
class Entry(BaseModel):
    title = CharField()
    date = CharField()
    time_spent = CharField()
    learned = TextField()
    resources = TextField()

    @property
    def ddate(self):
        _date = datetime.strptime(self.date, '%d/%m/%Y')
        return _date.strftime('%d/%m/%Y')
    
    @property
    def tdate(self):
        _date = datetime.strptime(self.date, '%d/%m/%Y')
        return _date.strftime('%B %d, %Y')

    class Meta:
        # Set DB table
        db_table = 'entries'