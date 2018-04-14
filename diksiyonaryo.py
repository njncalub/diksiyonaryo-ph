"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

Usage:
  diksiyonaryo.py init_db
  diksiyonaryo.py fetch (alphabet | words [<letter>])
  diksiyonaryo.py define <word>
  diksiyonaryo.py search <query>
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)

Options:
  -h, --help        Show this screen.
  -v, --version     Show version.
"""

from docopt import docopt

from config import settings
from main.utils import get_version, init_database


VERSION = (0, 1, 1)
__version__ = get_version(VERSION)


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    
    if settings.DEBUG:
        print(args)
    
    if args['init_db']:
        init_database()
    
    if args['fetch']:
        if args['alphabet']:
            pass
        if args['words']:
            pass
    
    if args['define']:
        pass
    
    if args['search']:
        pass
