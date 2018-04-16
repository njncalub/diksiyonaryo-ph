from sqlalchemy.ext.declarative import declarative_base

from main.utils import create_using_template, Connection


Base = declarative_base()

get_or_create_connection = create_using_template(template=Connection, base=Base)
