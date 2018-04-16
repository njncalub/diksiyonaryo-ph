import os
import pprint
import sys
from collections import Counter

from robobrowser import RoboBrowser
from simple_settings import LazySettings
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()


class Letter(Base):
    """
    A table for the letters. We created this model because "Ng" is a different
    consonant in Filipino and it should not show up as part of "N".
    """
    
    __tablename__ = 'Letter'
    
    CHOICES = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'Ñ', 'Ng', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    
    id = Column(Integer, primary_key=True)
    letter = Column(String, unique=True)


class Word(Base):
    """
    Holds the base word, its spelling, and its pronunciation.
    """
    
    __tablename__ = 'Word'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    cleaned = Column(String)
    pronunciation = Column(String)


class Sense(Base):
    """
    Holds the meaning. Words can have multiple meanings (senses).
    """
    
    __tablename__ = 'Sense'
    id = Column(Integer, primary_key=True)


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
                    self.create_database()
    
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
    
    def populate_alphabet(self):
        try:
            session = self.create_session()
            for ltr in Letter.CHOICES:
                res = session.query(Letter).filter(Letter.letter==ltr).all()
                if not res:
                    letter = Letter(letter=ltr)
                    session.add(letter)
            session.commit()
        except Exception as e:
            print(e)
            print(sys.exc_info())
            raise e
    
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


class Scraper(object):
    """
    Connects to the website and scrapes data from it. Saves data to the
    linked `Connection` object.
    """
    
    def __init__(self, connection, settings, printer, *args, **kwargs):
        self.connection = connection
        self.session = self.connection.create_session()
        
        self.BASE_URL = settings.SCRAPER_BASE_URL
        self.TEXT_NEXTBUTTON = settings.SCRAPER_TEXT_NEXTBUTTON
        self.URI_BYLETTER = settings.SCRAPER_URI_BYLETTER
        self.URI_BYLETTERPAGE = settings.SCRAPER_URI_BYLETTERPAGE
        self.SELECTOR_RESULTITEM = settings.SCRAPER_SELECTOR_RESULTITEM
        
        self.printer = printer
        self.browser = RoboBrowser(history=True, parser='html.parser')
    
    def process_word(self, W):
        classes = [value for element in W.find_all(class_=True)
                         for value in element["class"]]
        
        return Counter(classes)
        
        # self.printer(W, mode='pretty')
        
        # res = self.session.query(Word).filter(Word.title==W['id']).all()
        # if res:
        #     word = res[0]
        # else:
        #     word = Word(title=W['id'])
        #     self.session.add(word)
        #     self.session.commit()
        
        # self.printer(word.title, mode='pretty')
    
    def scrape_all(self, show_counter=False):
        self.printer('Fetching all words...')
        
        for letter in Letter.CHOICES:
            self.scrape_letter(letter, show_counter=show_counter)
        
        self.printer('Finished fetching.')
    
    def scrape_letter(self, letter, max_pages=None, counter=None,
                      show_counter=False):
        if not counter:
            counter = Counter()
        
        try:
            letter = self.format_letter(letter)
            url = self.URI_BYLETTER.format(base_url=self.BASE_URL,
                                           letter=letter)
            self.printer(f'Fetching words from "{url}"...')
            self.browser.open(url)
            
            total_words = 0
            page_count = 0
            current_url = url
            
            # iterate through all the pages
            while True:
                page_count = page_count + 1
                if max_pages:  # if max_pages is set, check it first
                    if page_count > max_pages:
                        break
                
                results = self.browser.select(self.SELECTOR_RESULTITEM)
                total_results = len(results)
                if not total_results:
                    break
                total_words = total_words + total_results
                
                for word in results:
                    counter = counter + self.process_word(word)
                
                # get link to next page
                next_page = self.browser.get_link(self.TEXT_NEXTBUTTON)
                next_page = next_page.get('href')
                if next_page.endswith('?page=0'):
                    break
                
                url = self.URI_BYLETTERPAGE.format(base_url=self.BASE_URL,
                                                   next_page=next_page)
                
                # open link if it is not the same with the current one
                if url != current_url:
                    # self.printer(f'Fetching words from "{url}"...')
                    self.browser.open(url)
                    current_url = url
                else:
                    break
            
            self.printer(f'> Letter "{letter}": processed ' \
                         f'{total_words} word(s) accross ' \
                         f'{page_count} page(s).')
        except Exception as e:
            print(e)
            print(sys.exc_info())
            raise e
        
        if show_counter:
            self.printer(counter, mode='pretty')
        
        return counter
    
    def format_letter(self, letter):
        return letter.title()
    
    def __str__(self):
        return "Scraper"


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
            print_text(with_prefix=True, *args, **kwargs)
            if color:
                self.add_format(color)
                self.add_format('BOLD')
            self.draw_line(char='%')
            self.add_format('END')
            print()
        elif footer:
            print_text(with_prefix=True, *args, **kwargs)
            self.draw_line()
        else:
            print_text(*args, **kwargs)
        
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

