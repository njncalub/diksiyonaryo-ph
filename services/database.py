import mongoengine

from data.models import Deriative, Letter, Meaning, PartOfSpeech, Word


def drop_database():
    Letter.drop_collection()
    PartOfSpeech.drop_collection()
    Word.drop_collection()


def load_letters():
    LETTERS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'Ñ', 'Ng', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
               'X', 'Y', 'Z')
    
    for char in LETTERS:
        results = Letter.objects().filter(letter=char)
        
        if not results:
            letter = Letter()
            letter.letter = char
            
            letter.save()


def load_parts_of_speech():
    TYPES = (
        'pangngalan',
        'panghalip',
        'pandiwa',
        'pang-uri',
        'pang-abay',
        'pangatnig',
        'pang-angkop',
        'pang-ukol',
    )
    
    for pos_type in TYPES:
        results = PartOfSpeech.objects().filter(pos=pos_type)
        
        if not results:
            pos = PartOfSpeech()
            pos.pos = pos_type
            
            pos.save()


def initialize_database():
    load_letters()
    load_parts_of_speech()


def clean_word(uncleaned: str) -> str:
    cleaned = uncleaned
    
    return cleaned


def create_word(**kwargs) -> Word:
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
            word.deriatves.append(create_deriatve(deriatve))
    
    # if kwargs.get('meanings'):
    #     for meaning in kwargs.get('meanings'):
    #         word.meanings.append(create_meaning(meaning))
    
    if kwargs.get('html'):
        word.html = kwargs.pop('html')
    
    word.save()
    
    return word


def create_meaning(meaning: dict) -> Meaning:
    meaning = Meaning()
    meaning.meaning = meaning.get('meaning', None)
    meaning.save()
    
    return meaning


def create_deriative(deriatve) -> Deriative:
    deriatve = Deriative()
    deriatve.save()
    
    return deriatve


def register_connection(host=None):
    if host:
        mongoengine.register_connection(alias='core', host=host)
    else:
        mongoengine.register_connection(alias='core', name='diksiyonaryo')
