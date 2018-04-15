import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main.utils import create_using_template


class Connection(object):
    """
    Using a Borg class for our database connection.
    """
    
    _shared_state = {}  # Borg design pattern's shared state.
    
    def __init__(self, base, database_url=None, create=False,
                 *args, **kwargs):
        self.__dict__ = self._shared_state
        
        # check if there is already a Borg instance.
        # if not, create a new one.
        if not self.__dict__.get('base'):
            self.base = base
            
            if database_url:
                self.database_url = database_url
                self.connect(database_url=self.database_url)
                
                if create:
                    create_database()
    
    def connect(self, database_url):
        try:
            self.engine = create_engine(database_url)
            self.base.metadata.bind = self.engine
            self.session_maker = sessionmaker(bind=self.engine)
        except Exception as e:
            msg = 'There is a problem in connecting to the database.'
            print(f'{msg} {e}')
            sys.exit(msg)
    
    def create_session(self):
        return self.session_maker()
    
    def create_database(self):
        if not self.base or not self.engine:
            raise NotImplementedError  # TODO: create custom exceptions
        self.base.metadata.create_all(self.engine)
    
    def __str__(self):
        return f'Connection(database_url={self.database_url})'


Base = declarative_base()

get_or_create_connection = create_using_template(template=Connection,
                                                 base=Base)
