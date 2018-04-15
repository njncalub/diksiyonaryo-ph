from os import getenv as env
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# Using a flag here to check if .proj-env should be loaded. We use .proj-env
# instead of .env to circumnavigate pipenv's default feature of automatically
# loading .env files in your project.
READ_DOT_PROJENV = env('READ_DOT_PROJENV', True)
DOT_PROJENV_FILENAME = env('DOT_PROJENV_FILENAME', '.proj-env')
DOT_PROJENV_OVERRIDE = env('DOT_PROJENV_OVERRIDE', False)

ROOT_DIR = Path(__file__) / '..' / '..'

if READ_DOT_PROJENV:
    ENV_PATH = find_dotenv(filename=DOT_PROJENV_FILENAME)
    load_dotenv(dotenv_path=ENV_PATH, override=DOT_PROJENV_OVERRIDE,
                verbose=True)

DEBUG = env('DEBUG', False)

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
DATABASE_URL = env('DATABASE_URL', 'sqlite:///db.sqlite3')

# ------------------------------------------------------------------------------
# Scraping
# ------------------------------------------------------------------------------
SCRAPER_BASE_URL = env('SCRAPER_BASE_URL', 'http://diksiyonaryo.ph')
SCRAPER_SELECTOR_PAGINATION = env('SCRAPER_SELECTOR_PAGINATION',
                                  '.pagination-list .page')
SCRAPER_SELECTOR_RESULTITEM = env('SCRAPER_SELECTOR_RESULTITEM', '.word')
SCRAPER_TEXT_NEXTBUTTON = env('SCRAPER_TEXT_NEXTBUTTON', '>>')
SCRAPER_URI_BYLETTER = env('SCRAPER_URI_BYLETTER', '{base_url}/list/{letter}')
SCRAPER_URI_BYLETTERPAGE = env('SCRAPER_URI_BYLETTERPAGE',
                               '{base_url}{next_page}')
