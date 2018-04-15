"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

Usage:
  diksiyonaryo.py [--settings=<file>] init_db
  diksiyonaryo.py [--settings=<file>] fetch (alphabet | words [<letter>])
  diksiyonaryo.py [--settings=<file>] define <word>
  diksiyonaryo.py [--settings=<file>] search <query>
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)
  diksiyonaryo.py test

Options:
  --settings=<file>  Use a different settings file [default: config.settings.local].
  -h, --help         Show this screen.
  -v, --version      Show version.
"""

import sys

from docopt import docopt
from simple_settings import LazySettings

from main.utils import get_version, init_database


# setting the version
VERSION = (0, 1, 1)
__version__ = get_version(VERSION)


def get_settings(filename=None):
    try:
        if not filename:
            raise NotImplementedError
        
        return LazySettings(filename)
    except NotImplementedError as e:
        sys.exit('No settings file provided.')
    except FileNotFoundError as e:
        sys.exit('Provided settings file does not exist.')
    except Exception as e:
        sys.exit('The application encountered an error during configuration.')

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    
    settings = get_settings(args['--settings'])
    
    if settings.DEBUG:
        print(f'Received arguments:\n{args}')
    
    if args['init_db']:
        init_database()
    
    if args['fetch']:
        if args['alphabet']:
            raise NotImplementedError
        if args['words']:
            raise NotImplementedError
    
    if args['define']:
        raise NotImplementedError
    
    if args['search']:
        raise NotImplementedError
