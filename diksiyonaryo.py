#!/usr/bin/env python
# coding=utf-8

"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

Usage:
  diksiyonaryo.py [options] init
  diksiyonaryo.py [options] fetch [<letter>]
  diksiyonaryo.py [options] define <word>
  diksiyonaryo.py [options] search <query>
  diksiyonaryo.py [options] run
  diksiyonaryo.py [options] shell
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)
  diksiyonaryo.py test

Options:
  --settings=<file>  Use a different settings file
                     [default: config.settings.local].
  --start=<page>     When fetching, specify which page to start at [default: 0].
  --end=<page>       When fetching, specify which page to end.
  --max-pages=<max>  Set an upper limit on how many pages the scraper will
                     fetch, per letter.
  --debug            Force debug mode.
  -q, --quiet        Decrease amount of text shown [default: False].
  -h, --help         Show this help message and exit.
  -v, --version      Show version and exit.
"""

import sys
import time

from docopt import docopt

from utils.printer import init_printer
from utils.settings import load_settings
from utils.version import format_version
from services.database import register_connection
from services.server import run_server
from services.scraper import get_or_create_scraper, Scraper


HEADER = """
██████╗ ██╗██╗  ██╗     ███████╗██╗    ██╗   ██╗ ██████╗
██╔══██╗██║██║ ██╔╝     ██╔════╝██║    ╚██╗ ██╔╝██╔═══██╗
██║  ██║██║█████╔╝  ██╗ ███████╗██║ ██╗ ╚████╔╝ ██║   ██║
██║  ██║██║██╔═██╗  ╚═╝ ╚════██║██║ ╚═╝  ╚██╔╝  ██║   ██║
██████╔╝██║██║  ██╗     ███████║██║       ██║   ╚██████╔╝
╚═════╝ ╚═╝╚═╝  ╚═╝ ▄▀  ╚══════╝╚═╝       ╚═╝    ╚═════╝
       ███╗   ██╗ █████╗ ██████╗     ██╗   ██╗ ██████╗
       ████╗  ██║██╔══██╗██╔══██╗    ╚██╗ ██╔╝██╔═══██╗
       ██╔██╗ ██║███████║██████╔╝ ██╗ ╚████╔╝ ██║   ██║
       ██║╚██╗██║██╔══██║██╔══██╗ ╚═╝  ╚██╔╝  ██║   ██║
       ██║ ╚████║██║  ██║██║  ██║       ██║   ╚██████╔╝
       ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝"""
VERSION = (0, 1, 1)
__version__ = format_version(VERSION)


printer = None


def run_shell():
    try:
        while True:
            pass
    except KeyboardInterrupt:
        return


def establish_db_connection():
    printer('Establishing the database connection...')
    register_connection()


def populate_database():
    printer('Populating the database...')
    pass

def define_word(word):
    pass


def search_query(query):
    pass


def start_test():
    try:
        import pytest
    except ImportError as e:
        printer('pytest required.', style='error')
    
    printer('Running tests...')
    pytest.main(['-v', '-x', 'tests'])


def fetch_all(scraper: Scraper, start: int, end: int):
    printer(f'Fetching from {settings.SCRAPER_BASE_URL}...')
    
    scraper.scrape_all()


def fetch_letter(scraper: Scraper, start: int, end: int):
    printer(f'Fetching from {settings.SCRAPER_BASE_URL}...')
    
    scraper.scrape_letter(letter=args['<letter>'],
                          max_pages=args['--max-pages'])


def show_debug_info(*args, **kwargs):
    if kwargs.get('args', None):
        printer('Received the following arguments:')
        printer(kwargs.get('args'), mode='pretty')
    
    if kwargs.get('settings', None):
        printer('Using the following settings:')
        printer(kwargs.get('settings').as_dict(), mode='pretty')


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    settings = load_settings(filename=args['--settings'])
    printer = init_printer(is_quiet=args['--quiet'])
    
    printer('Starting the application...')
    establish_db_connection()
    time.sleep(3)
    
    try:
        if settings.DEBUG or args['--debug']:
            show_debug_info(args=args, settings=settings)
        
        if args['init']:
            populate_database()
        elif args['fetch']:
            scraper = get_or_create_scraper(settings=settings, printer=printer)
            
            if args['<letter>']:
                fetch_letter(scraper=scraper, start=args['--start'],
                             end=args['--end'])
            else:
                fetch_all(scraper=scraper, start=args['--start'],
                          end=args['--end'])
        elif args['define']:
            define_word(word=args['<word>'])
        elif args['search']:
            search_query(query=args['<query>'])
        elif args['test']:
            search_query()
        elif args['run']:
            run_server()
        elif args['shell']:
            run_shell()
    except Exception as e:
        printer('Finished with errors.', msg_type='header', style='error')
        printer(e, mode='pretty')
        printer(sys.exc_info())
    else:
        printer('Finished successfully.', msg_type='header', style='success')

