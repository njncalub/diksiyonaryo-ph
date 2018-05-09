#!/usr/bin/env python
# coding=utf-8

"""Diksiyonaryo CLI (https://github.com/njncalub/diksiyonaryo-ph).

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
       ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝

Usage:
  diksiyonaryo.py [options] (init | drop)
  diksiyonaryo.py [options] fetch [<letter>]
  diksiyonaryo.py [options] define <word>
  diksiyonaryo.py [options] search <query>
  diksiyonaryo.py [options] run [<host> <port>]
  diksiyonaryo.py [options] shell
  diksiyonaryo.py (-h | --help)
  diksiyonaryo.py (-v | --version)
  diksiyonaryo.py test

Options:
  --settings=<file>  Use a different settings file
                     [default: config.settings.local].
  --start=<page>     When fetching, specify which page to start at
                     [default: 0].
  --end=<page>       When fetching, specify which page to end.
  --max-pages=<max>  Set an upper limit on how many pages the scraper will
                     fetch, per letter.
  --from=<letter>    When fetching all letters, specify a letter to start at.
  --to=<letter>      When fetching all letters, specify a letter to end at.
  --debug            Force debug mode.
  -q, --quiet        Decrease amount of text shown [default: False].
  -h, --help         Show this help message and exit.
  -v, --version      Show version and exit.
"""

from docopt import docopt

from app import DiksiyonaryoApp, __version__
from utils.settings import load_settings


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    settings = load_settings(filename=args['--settings'])
    
    app = DiksiyonaryoApp(settings=settings, is_quiet=args['--quiet'])
    
    if args['init']:
        app.run_init_db()
    elif args['drop']:
        app.run_drop_db()
    elif args['fetch']:
        if args['<letter>']:
            app.run_fetch_letter(letter=args['<letter>'],
                                 max_pages=args['--max-pages'],
                                 start=args['--start'], end=args['--end'])
        else:
            app.run_fetch_all(start=args['--start'], end=args['--end'],
                              from_letter=args['--from'],
                              to_letter=args['--to'])
    elif args['define']:
        app.run_define(word=args['<word>'])
    elif args['search']:
        app.run_search(query=args['<query>'])
    elif args['test']:
        app.run_test()
    elif args['run']:
        options = {
            'host': args['<host>'] or settings.API_SERVER_HOST,
            'port': args['<port>'] or settings.API_SERVER_PORT,
            'debug': args['--debug'] or settings.API_SERVER_DEBUG,
        }
        app.run_server(**options)
    elif args['shell']:
        app.run_shell()
