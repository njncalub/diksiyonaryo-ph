from apistar.server.components import Component

from services.database import Database
from utils.database import init_database_service


class DatabaseComponent(Component):
    def resolve(self) -> Database:
        return init_database_service()


components = [DatabaseComponent()]
