import api.server
from utils.database import init_database_service
from utils.settings import load_settings


settings = load_settings()
database = init_database_service(host=settings.DATABASE_URL)

application = api.server.create_app()
