import sys

import mongoengine

from data.models import Deriative, Letter, Meaning, PartOfSpeech, Word


class Database(object):
    """
    A Borg object that you only need to instantiate once.
    """
    
    __shared_state = {}  # Borg design pattern's shared state.
    __initialized = False
    
    def __init__(self, host=None, *args, **kwargs):
        self.__dict__ = self.__shared_state
        
        try:
            # exit if already instantiated
            if self.__initialized:
                return
            else:
                self.__initialized = True
            
            if host:
                self.host = host
                self.register_connection(host=self.host)
            else:
                self.register_connection()
        except Exception as e:
            print(e)
            print(sys.exc_info())
    
    def drop_database(self):
        used_models = [
            Letter,
            PartOfSpeech,
            Word,
        ]
        
        for model in used_models:
            model.drop_collection()
    
    def load_letters(self):
        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'Ñ', 'Ng', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                   'W', 'X', 'Y', 'Z')
        
        for letter in letters:
            results = Letter.objects().filter(letter=letter)
            
            if not results:
                new_letter = Letter(letter=letter)
                new_letter.save()
    
    def load_parts_of_speech(self):
        parts = (
            'pangngalan',
            'panghalip',
            'pandiwa',
            'pang-uri',
            'pang-abay',
            'pangatnig',
            'pang-angkop',
            'pang-ukol',
        )
        
        for part in parts:
            results = PartOfSpeech.objects().filter(pos=part)
            
            if not results:
                new_pos = PartOfSpeech(pos=part)
                new_pos.save()
    
    def initialize_database(self):
        self.load_letters()
        self.load_parts_of_speech()
    
    def clean_word(self, uncleaned: str) -> str:
        # TODO: not yet working
        cleaned = uncleaned
        return cleaned
    
    def create_word(self, **kwargs) -> Word:
        word = Word()
        
        if kwargs.get('entry'):
            word.entry = kwargs.pop('entry')
        else:
            raise NotImplemented
        
        if kwargs.get('cleaned_entry'):
            word.cleaned_entry = kwargs.pop('cleaned_entry')
        
        if kwargs.get('pos'):
            word.pos = kwargs.pop('pos')
        
        if kwargs.get('pronunciation'):
            word.pronunciation = kwargs.pop('pronunciation')
        
        if kwargs.get('alt_pronunciation'):
            word.alt_pronunciation = kwargs.pop('alt_pronunciation')
        
        if kwargs.get('deriatives'):
            for deriatve in kwargs.get('deriatives'):
                word.deriatves.append(self.create_deriatve(deriatve))
        
        # if kwargs.get('meanings'):
        #     for meaning in kwargs.get('meanings'):
        #         word.meanings.append(self.create_meaning(meaning))
        
        if kwargs.get('html'):
            word.html = kwargs.pop('html')
        
        word.save()
        
        return word
    
    def create_meaning(self, meaning: dict) -> Meaning:
        meaning = Meaning()
        meaning.meaning = meaning.get('meaning', None)
        meaning.save()
        
        return meaning
    
    def create_deriative(self, deriatve) -> Deriative:
        deriatve = Deriative()
        deriatve.save()
        
        return deriatve
    
    def register_connection(self, host=None):
        if host:
            mongoengine.register_connection(alias='core', host=host)
        else:
            mongoengine.register_connection(alias='core', name='diksiyonaryo')
    
    def find_words(self, matching: str=None):
        if matching:
            return Word.objects.filter(cleaned_entry__icontains=matching)
        return Word.objects.all()
    
    def find_word(self, entry):
        return Word.objects.get(cleaned_entry=entry)
