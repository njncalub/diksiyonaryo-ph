from apistar import Route, Include

from .words import routes as words_routes


routes = [
    Include('/words', name='words', routes=words_routes),
]
