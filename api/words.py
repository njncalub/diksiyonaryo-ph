import typing

from apistar import App, Route, exceptions

from .types import Word as WordType

from data.models import Word


def list_words(app: App) -> typing.List:
    queryset = Word.objects.all()
    
    return [
        {
            'word': WordType(word.serialize()),
            'url': app.reverse_url('word:get_word', entry=entry)
        } for word in queryset
    ]


def get_word(app: App, entry: str) -> dict:
    found = Word.objects.filter(entry=entry)
    if not found:
        raise exceptions.NotFound()
    
    return {
        'word': found.first().serialize(),
        'url': app.reverse_url('word:get_word', entry=entry)
    }


routes = [
    Route('/', method='GET', handler=list_words),
    Route('/{entry}', method='GET', handler=get_word),
]
