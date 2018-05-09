from services import Database


def init_database_service(host):
    svc = Database(host=host)
    
    return svc
