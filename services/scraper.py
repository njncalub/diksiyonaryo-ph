from robobrowser import RoboBrowser
from unidecode import unidecode

from data.models import Word
from services.database import create_word


class Scraper(object):
    """
    Connects to the website and scrapes data from it.
    """
    
    HISTORY = False
    PARSER = 'html.parser'
    LETTERS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'Ñ', 'Ng', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z')
    
    def __init__(self, *args, **kwargs):
        options = {
            'base_url': 'http://diksiyonaryo.ph',
            'next_button_text': '>>',
            'letter_list_uri': '{base_url}/list/{letter}',
            'letter_list_page_uri': '{base_url}{next_page}',
            'result_item_selector': '.word',
            'printer': None,
        }
        options.update(kwargs)
        
        for key in options:
            self.__setattr__(key, options[key])
        
        self.browser = RoboBrowser(history=self.HISTORY, parser=self.PARSER)
    
    def process_letter(self, letter: str):
        return letter.title()
    
    def clean_accents(self, text):
        text = unidecode(text).strip()
        
        return text
    
    def process_result(self, tag):
        data = {
            'entry': tag.get('id', None).strip(),
            'cleaned': self.clean_accents(tag.get('id', None)),
            'pos': tag.find(class_='pos').string.strip(),
            'pronounciation': tag.find(class_='pronunciation').string.strip(),
            'html': tag.decode(),
        }
        
        # loop through all the senses
        print('Looping through all the senses:')
        for sense in tag.find_all(class_='sense'):
            pass
        
        results = Word.objects().filter(entry=data.get('entry'))
        if not results:
            word = create_word(**data)
            return word
    
    def scrape_all(self, start: int = None, end: int = None):
        self.printer('Fetching all words...')
        
        for letter in self.LETTERS:
            self.scrape_letter(letter)
        
        self.printer('Finished fetching.')
    
    def scrape_letter(self, letter: str, max_pages: int = None,
                     start: int = None, end: int = None):
        letter = self.process_letter(letter)
        
        url = self.letter_list_uri.format(base_url=self.base_url,
                                       letter=letter)
        self.printer(f'Fetching words from "{url}"...')
        self.browser.open(url)
        
        total_words = 0
        page_count = 0
        current_url = url
        
        while True:
            page_count = page_count + 1
            if max_pages and page_count > max_pages:
                break
            
            results = self.browser.select(self.result_item_selector)
            total_results = len(results)
            if not total_results:
                break
            total_words = total_words + total_results
            
            # for tag in results:
                # self.process_result(tag)
            self.process_result(results[0])
            
            # get link to next page
            next_page = self.browser.get_link(self.next_button_text)
            next_page = next_page.get('href')
            if next_page.endswith('?page=0'):
                break
            
            url = self.letter_list_page_uri.format(base_url=self.base_url,
                                               next_page=next_page)
            
            # exit if url is the same
            if url == current_url:
                break
            
            self.printer(f'Fetching words from "{url}"...')
            self.browser.open(url)
            current_url = url
    
    def __str__(self):
        return 'Scraper'


def get_or_create_scraper(settings, printer, *args, **kwargs) -> Scraper:
    options = {
        'base_url': settings.SCRAPER_BASE_URL,
        'next_button_text': settings.SCRAPER_TEXT_NEXTBUTTON,
        'letter_list_uri': settings.SCRAPER_URI_BYLETTER,
        'letter_list_page_uri': settings.SCRAPER_URI_BYLETTERPAGE,
        'result_item_selector': settings.SCRAPER_SELECTOR_RESULTITEM,
        'printer': printer,
    }
    
    return Scraper(**options)
