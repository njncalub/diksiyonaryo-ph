from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from envparse import Env

# configure env schema, describe all non-str
env = Env(READ_DOT_PROJENV=bool,
          DOT_PROJENV_OVERRIDE=bool,
          DEBUG=bool,
          SCRAPER_PAGINATION_DIVIDER=int)

# Using a flag here to check if .proj-env should be loaded. We use .proj-env
# instead of .env to circumnavigate pipenv's default feature of automatically
# loading .env files in your project.
READ_DOT_PROJENV = env('READ_DOT_PROJENV', default=True)
DOT_PROJENV_FILENAME = env('DOT_PROJENV_FILENAME', default='.proj-env')
DOT_PROJENV_OVERRIDE = env('DOT_PROJENV_OVERRIDE', default=False)

ROOT_DIR = Path(__file__) / '..' / '..' / '..'

if READ_DOT_PROJENV:
    ENV_PATH = find_dotenv(filename=DOT_PROJENV_FILENAME)
    load_dotenv(dotenv_path=ENV_PATH, override=DOT_PROJENV_OVERRIDE,
                verbose=True)

DEBUG = env('DEBUG', default=False)

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
DATABASE_URL = env('DATABASE_URL', default='sqlite:///db.sqlite3')

# ------------------------------------------------------------------------------
# Scraping
# ------------------------------------------------------------------------------
SCRAPER_BASE_URL = env('SCRAPER_BASE_URL', default='http://diksiyonaryo.ph')
SCRAPER_SELECTOR_PAGINATION = env('SCRAPER_SELECTOR_PAGINATION',
                                  default='.pagination-list .page')
SCRAPER_SELECTOR_RESULTITEM = env('SCRAPER_SELECTOR_RESULTITEM',
                                  default='.word')
SCRAPER_PAGINATION_DIVIDER = env('SCRAPER_PAGINATION_DIVIDER', default=4)
SCRAPER_TEXT_NEXTBUTTON = env('SCRAPER_TEXT_NEXTBUTTON', default='>>')
SCRAPER_URI_BYLETTER = env('SCRAPER_URI_BYLETTER',
                           default='{base_url}/list/{letter}')
SCRAPER_URI_BYLETTERPAGE = env('SCRAPER_URI_BYLETTERPAGE',
                               default='{base_url}{next_page}')
