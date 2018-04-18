import datetime
import bson
from typing import List

import mongoengine

from data.models import Deriative, Meaning, Word


def clean_word(uncleaned: str) -> str:
    cleaned = uncleaned
    
    return cleaned


def create_word(**kwargs) -> Word:
    word = Word()
    
    if kwargs.get('entry'):
        word.entry = kwargs.pop('entry')
    else:
        raise NotImplemented
    
    if kwargs.get('cleaned'):
        word.cleaned = kwargs.pop('cleaned')
    
    if kwargs.get('html'):
        word.html = kwargs.pop('html')
    
    if kwargs.get('pronunciation'):
        word.pronunciation = kwargs.pop('pronunciation')
    
    if kwargs.get('alt_pronunciation'):
        word.alt_pronunciation = kwargs.pop('alt_pronunciation')
    
    if kwargs.get('meanings'):
        for meaning in kwargs.get('meanings'):
            word.meanings.append(create_meaning(meaning))
    
    word.save()
    
    return word


def create_meaning(meaning: dict) -> Meaning:
    meaning = Meaning()
    meaning.save()
    
    return meaning


def register_connection():
    mongoengine.register_connection(alias='core', name='diksiyonaryo')
