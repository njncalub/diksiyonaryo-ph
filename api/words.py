import typing

from apistar import App, Route, exceptions, http
from apistar_mongoengine.pagination import Pagination

from services import Database


def list_words(app: App, db: Database, page: int=1,
               q: str=None) -> typing.List:
    PAGE_SIZE = 20
    
    queryset = db.find_words(matching=q)
    paginated = Pagination(iterable=queryset, page=page, per_page=PAGE_SIZE)
    
    return [word.serialize(app=app) for word in paginated.items]


def get_word(app: App, db: Database, entry: str) -> dict:
    word = db.find_word(entry=entry)
    if not word:
        raise exceptions.NotFound()
    
    return word.serialize(app=app)


routes = [
    Route('/', method='GET', handler=list_words),
    Route('/{entry}', method='GET', handler=get_word),
]
