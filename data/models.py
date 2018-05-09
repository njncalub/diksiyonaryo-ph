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
    
    def __repr__(self):
        return 'Letter(letter="{}")'.format(self.letter)
    
    def serialize(self):
        return {
            'letter': self.letter,
        }


class PartOfSpeech(Document):
    pos = StringField(required=True)
    
    meta = {
        'db_alias': 'core',
        'collection': 'parts',
    }
    
    def __repr__(self):
        return 'PartOfSpeech(pos="{}")'.format(self.pos)
    
    def serialize(self):
        return {
            'pos': self.pos,
        }


class Deriative(EmbeddedDocument):
    entry = StringField(required=True)
    
    def __repr__(self):
        return 'Deriative(entry="{}")'.format(self.entry)
    
    def serialize(self):
        return {
            'entry': self.entry,
        }


class Meaning(EmbeddedDocument):
    meaning = StringField(required=True)
    example = StringField(required=False)
    
    def __repr__(self):
        return 'Meaning(meaning="{}", example="{}")'.format(self.meaning,
                                                            self.example)
    
    def serialize(self):
        return {
            'meaning': self.meaning,
            'example': self.example,
        }


class Word(Document):
    entry = StringField(required=True)
    cleaned_entry = StringField(required=True)
    pos = StringField(required=False)
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
    
    def __repr__(self):
        return 'Word(entry="{}")'.format(self.entry)
    
    def serialize(self, app):
        return {
            'entry': self.entry,
            'cleaned_entry': self.cleaned_entry,
            'pos': self.pos,
            'pronunciation': self.pronunciation,
            'alt_pronunciation': self.alt_pronunciation,
            'deriatives': self.deriatives,
            'meanings': self.meanings,
            'html': self.html,
            'created_date': str(self.created_date),
            'url': app.reverse_url('words:get_word', entry=self.entry)
        }
