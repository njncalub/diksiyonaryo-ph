"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

Usage:
  diksiyonaryo.py [options] init
  diksiyonaryo.py [options] fetch (all | alphabet | words [<letter>])
  diksiyonaryo.py [options] define <word>
  diksiyonaryo.py [options] search <query>
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)
  diksiyonaryo.py run

Options:
  --settings=<file>  Use a different settings file
                     [default: config.settings.local].
  -q, --quiet        When DEBUG=True, decrease amount of text shown in the logs
                     [default: False].
  -h, --help         Show this help message and exit.
  -v, --version      Show version and exit.
"""

import sys

from docopt import docopt

from main.models import get_or_create_connection
from main.utils import format_version, get_settings, Printer


VERSION = (0, 1, 1)


if __name__ == '__main__':
    args = docopt(__doc__, version=format_version(VERSION))
    settings = get_settings(filename=args['--settings'])
    
    printer = Printer(is_quiet=args['--quiet'])
    
    if settings.DEBUG:
        printer('Received arguments:', header=True)
        printer(args, mode='pretty')
        printer('Using the following settings:', header=True)
        printer(settings.as_dict(), mode='pretty')
    
    connection = get_or_create_connection(database_url=settings.DATABASE_URL)
    
    if args['init']:
        printer('Initializing the database...', header=True)
        connection.create_database()
    
    if args['fetch']:
        if args['alphabet']:
            raise NotImplementedError
        if args['words']:
            raise NotImplementedError
    
    if args['define']:
        raise NotImplementedError
    
    if args['search']:
        raise NotImplementedError
    
    if args['run']:
        raise NotImplementedError
    
    printer('Finished successfully.')
