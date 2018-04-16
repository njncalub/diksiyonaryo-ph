import os
import pprint
import sys

from simple_settings import LazySettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
        try:
            if not self.__dict__.get('base') or not self.__dict__.get('engine'):
                raise NotImplementedError  # TODO: create custom exceptions
            self.base.metadata.create_all(self.engine)
        except NotImplementedError as e:
            print('Error: Base and engine not set. Initialize database first.')
            print(sys.exc_info())
        except Exception as e:
            print(sys.exc_info())
    
    def __str__(self):
        return f'Connection(database_url={self.database_url})'


class ProjectSettings(object):
    """
    A Borg ProjectSettings object that you only need to instantiate once.
    """
    
    __shared_state = {}  # Borg design pattern's shared state.
    
    def __init__(self, filename=None, *args, **kwargs):
        self.__dict__ = self.__shared_state
        
        try:
            # check if object was already instantiated
            if self.__dict__.get('filename') and self.__dict__.get('config'):
                return
            
            if filename:
                self.filename = filename
                self.config = LazySettings(self.filename)
            else:
                raise NotImplementedError
        except NotImplementedError as e:
            print('Please pass a filename first.')
            print(sys.exc_info())
        except Exception as e:
            print(sys.exc_info())
    
    def __getattr__(self, key):
        """
        Called if there is no class attribute found on the object.
        """
        try:
            if self.config:
                return self.config.as_dict().get(key)
            else:
                raise NotImplementedError
        except NotImplementedError as e:
            print('LazySettings not yet created.')
            print(sys.exc_info())
        except Exception as e:
            print(sys.exc_info())
    
    def __str__(self):
        return f'ProjectSettings(filename={self.filename})'
    
    def as_dict(self):
        if self.config:
            return self.config.as_dict()
        else:
            return {}

class Printer(object):
    """
    A Borg Printer that only prints when --quiet is not True.
    
    TODO: refactor to have better templates.
    TODO: refactor to use multiple values in __call__.
    """
    
    __shared_state = {}  # Borg design pattern's shared state.
    
    def __init__(self, is_quiet=False, pretty=None, indent=1, noline=False,
                 prefix=None, *args, **kwargs):
        self.__dict__ = self.__shared_state
        self.is_quiet = is_quiet
        self.noline = noline
        self.prefix = prefix if prefix else '✨ '
        if not pretty:
            self.pretty = pprint.PrettyPrinter(indent=indent).pprint
        else:
            self.pretty = pretty
    
    def __call__(self, value=None, mode=None, header=False, footer=False,
                 endline=False, color=None, *args, **kwargs):
        if self.is_quiet:
            return
        
        if not value:  # default behavior when value is blank
            self.draw_line()
            return
        
        def print_text(with_prefix=False, *args_, **kwargs_):
            if with_prefix:
                print(self.prefix, end='')
            
            if not mode:
                print(value, *args_, **kwargs_)
            elif mode is 'pretty':
                self.pretty(value, *args_, **kwargs_)
        
        if header:
            print()
            if color:
                self.add_format(color)
            self.add_format('BOLD')
            self.draw_line(char='%')
            if color:
                self.add_format('END')
                self.add_format('BOLD')
            print_text(with_prefix=True)
            if color:
                self.add_format(color)
                self.add_format('BOLD')
            self.draw_line(char='%')
            self.add_format('END')
            print()
        elif footer:
            print_text(with_prefix=True)
            self.draw_line()
        else:
            print_text()
        
        if endline:
            self.draw_line()
    
    def __str__(self):
        return f'Printer(is_quiet={self.is_quiet})'
    
    def draw_line(self, char=None, n=None):
        if self.noline:
            return
        char = char if char else '='
        n = n if n else os.get_terminal_size().columns
        print(char * n)
    
    def add_format(self, code, end=None):
        """
        Taken from https://stackoverflow.com/a/17303428
        """
        colors = {
            'PURPLE': '\033[95m',
            'CYAN': '\033[96m',
            'DARKCYAN': '\033[36m',
            'BLUE': '\033[94m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'END': '\033[0m',
        }
        end = end if end else ''
        print(colors.get(code), end=end)


def format_version(v):
    """
    Return a PEP 440-compliant version number from VERSION.
    
    Using "major.minor.micro" versioning.
    """
    
    version = f'{v[0]}.{v[1]}.{v[2]}'
    
    return version

def create_using_template(template, base):
    """
    A little utility function that creates an object, and passes a Base.
    """
    
    def _create_using_template(*args, **kwargs):
        return template(base=base, *args, **kwargs)
    
    return _create_using_template
