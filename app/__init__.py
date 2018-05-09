from .version import VERSION

from utils.api import run_api_server
from utils.database import init_database_service
from utils.printer import init_printer_service
from utils.scraper import init_scraper_service
from utils.version import format_version


__version__ = format_version(VERSION)


class DiksiyonaryoApp(object):
    """
    Main application that handles the scraping, processing, and serving of the
    data.
    """
    
    def __init__(self, settings, is_quiet=False, *args, **kwargs):
        print('Initializing the Diksiyonaryo App:')
        
        self.settings = settings
        
        self.setup_printer_service(is_quiet=is_quiet)
        self.setup_db_service()
        self.setup_scraper_service()
        
        print('-' * 30)
    
    def setup_printer_service(self, is_quiet):
        print('> Setting up the printer...')
        self.printer = init_printer_service(is_quiet=is_quiet)
    
    def setup_db_service(self):
        print('> Setting up the database connection...')
        self.db = init_database_service(host=self.settings.DATABASE_URL)
    
    def setup_scraper_service(self):
        print('> Setting up the scraper...')
        options = {
            'base_url': self.settings.SCRAPER_BASE_URL,
            'next_button_text': self.settings.SCRAPER_TEXT_NEXTBUTTON,
            'letter_list_uri': self.settings.SCRAPER_URI_BYLETTER,
            'letter_list_page_uri': self.settings.SCRAPER_URI_BYLETTERPAGE,
            'result_item_selector': self.settings.SCRAPER_SELECTOR_RESULTITEM,
            'printer': self.printer,
            'db': self.db,
        }
        
        self.scraper = init_scraper_service(**options)
    
    def run_shell(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            return
    
    def run_server(self, host=None, port=None, debug=False):
        if port:
            try:
                port = int(port)
            except:
                pass
        
        run_api_server(host=host, port=port, debug=debug)
    
    def run_init_db(self):
        print('Populating the database...')
        self.db.initialize_database()
    
    def run_drop_db(self):
        print('Dropping the database...')
        self.db.drop_database()
    
    def run_define(self, word):
        pass
    
    def run_search(self, query):
        pass
    
    def run_test(self):
        try:
            import pytest
            print('Running tests...')
            pytest.main(['-v', '-x', 'tests'])
        except ImportError as e:
            print('pytest required.')
    
    def run_fetch_all(self, start=None, end=None, from_letter=None,
                      to_letter=None):
        self.scraper.scrape_all(start=start, end=end, from_letter=from_letter,
                                to_letter=to_letter)
    
    def run_fetch_letter(self, letter=None, max_pages=None, start=None,
                         end=None):
        self.scraper.scrape_letter(letter=letter, max_pages=max_pages)
