import datetime

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
)


class Deriative(EmbeddedDocument):
    entry = StringField(required=True)


class Meaning(EmbeddedDocument):
    meaning = StringField(required=True)


class Word(Document):
    entry = StringField(required=True)
    cleaned = StringField(required=True)
    pronunciation = StringField(required=False)
    alt_pronunciation = StringField(required=False)
    
    deriatives = EmbeddedDocumentListField(Deriative)
    meanings = EmbeddedDocumentListField(Meaning)
    
    html = StringField()
    created_date = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'db_alias': 'core',
        'collection': 'words'
    }
