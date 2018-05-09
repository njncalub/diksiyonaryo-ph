from services import Database


def init_database_service(host=None) -> Database:
    return Database(host=host)
