import typing

from apistar import App, Route, exceptions

from services import Database


def list_words(app: App, db: Database) -> typing.List[dict]:
    queryset = db.get_words()
    
    return [word.serialize(app=app) for word in queryset]


def get_word(app: App, db: Database, entry: str) -> dict:
    word = db.get_word(entry=entry)
    if not word:
        raise exceptions.NotFound()
    
    return word.serialize(app=app)


routes = [
    Route('/', method='GET', handler=list_words),
    Route('/{entry}', method='GET', handler=get_word),
]
