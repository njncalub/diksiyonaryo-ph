import datetime

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
)


class Letter(Document):
    letter = StringField(required=True)
    
    meta = {
        'db_alias': 'core',
        'collection': 'letters',
    }


class PartOfSpeech(Document):
    pos = StringField(required=True)
    
    meta = {
        'db_alias': 'core',
        'collection': 'parts',
    }


class Deriative(EmbeddedDocument):
    entry = StringField(required=True)


class Meaning(EmbeddedDocument):
    meaning = StringField(required=True)
    example = StringField(required=False)


class Word(Document):
    entry = StringField(required=True)
    cleaned_entry = StringField(required=True)
    pos = StringField(required=True)
    pronunciation = StringField(required=False)
    alt_pronunciation = StringField(required=False)
    deriatives = EmbeddedDocumentListField(Deriative)
    meanings = EmbeddedDocumentListField(Meaning)
    html = StringField()
    created_date = DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'db_alias': 'core',
        'collection': 'words',
    }
