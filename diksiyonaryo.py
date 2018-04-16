"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

Usage:
  diksiyonaryo.py [options] init
  diksiyonaryo.py [options] fetch [<letter>]
  diksiyonaryo.py [options] define <word>
  diksiyonaryo.py [options] search <query>
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)
  diksiyonaryo.py test
  diksiyonaryo.py run

Options:
  --settings=<file>  Use a different settings file
                     [default: config.settings.local].
  --max-pages=<max>  Set an upper limit on how many pages the scraper will
                     fetch, per letter.
  -q, --quiet        When DEBUG=True, decrease amount of text shown in the logs
                     [default: False].
  -h, --help         Show this help message and exit.
  -v, --version      Show version and exit.
"""

import os
import sys

from docopt import docopt

from main.utils import format_version, get_or_create_connection
from main.models import Printer, ProjectSettings, Scraper


VERSION = (0, 1, 1)
__version__ = format_version(VERSION)

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    
    settings = ProjectSettings(filename=args['--settings'])
    printer = Printer(is_quiet=args['--quiet'])
    
    printer('Starting the application...')
    
    try:
        # if settings.DEBUG:
        #     printer('Received the following arguments:', header=True)
        #     printer(args, mode='pretty')
        #     printer('Using the following settings:', header=True)
        #     printer(settings.as_dict(), mode='pretty')
        
        connection = get_or_create_connection(
            database_url=settings.DATABASE_URL)
        
        if args['init']:
            printer('Initializing the database...', header=True)
            connection.create_database()
            connection.populate_alphabet()
        
        if args['fetch']:
            printer(f'Fetching from {settings.SCRAPER_BASE_URL}...',
                    header=True)
            scraper = Scraper(connection=connection, settings=settings,
                              printer=printer)
            
            if args['<letter>']:
                scraper.scrape_letter(letter=args['<letter>'],
                                      max_pages=args['--max-pages'])
            else:  # default: all
                scraper.scrape_all()
        
        if args['define']:
            raise NotImplementedError
        
        if args['search']:
            raise NotImplementedError
        
        if args['test']:
            try:
                import pytest
            except ImportError as e:
                print(sys.exc_info())
            
            printer('Running tests...', header=True)
            pytest.main(['-v', '-x', 'tests'])
        
        if args['run']:
            raise NotImplementedError
    except Exception as e:
        printer('Finished with errors.', header=True, color='RED')
    else:
        printer('Finished successfully.', header=True, color='GREEN')
