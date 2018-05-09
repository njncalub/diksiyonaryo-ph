from robobrowser import RoboBrowser
from unidecode import unidecode

from data.models import Letter, Word


class Scraper(object):
    """
    Connects to the website and scrapes data from it.
    """
    
    def __init__(self, *args, **kwargs):
        options = {
            'base_url': 'http://diksiyonaryo.ph',
            'next_button_text': '>>',
            'letter_list_uri': '{base_url}/list/{letter}',
            'letter_list_page_uri': '{base_url}{next_page}',
            'result_item_selector': '.word',
            'printer': None,
            'history': False,
            'parser': 'html.parser',
            'db': None,
        }
        options.update(kwargs)
        
        for key in options:
            self.__setattr__(key, options[key])
        
        self.browser = RoboBrowser(history=self.history, parser=self.parser)
    
    def process_letter(self, letter: str):
        return letter.title()
    
    def clean_accents(self, text):
        text = unidecode(text).strip()
        
        return text
    
    def process_alt_pronunciation(self, tag=None):
        if not tag:
            return None
        
        text = tag.string.strip()
        # TODO: remove parentheses
        
        return text
    
    def process_pronunciation(self, tag):
        if not tag:
            return None
        
        text = tag.string.strip()
        
        return text
    
    def process_sense(self, item):
        # definition_text = item.find(class_='definition-text')
        # print(definition_text)
        # print()
        # if definition_text:
        #     text = definition_text.string.strip()
        #     print(text)
        #     print()
        pass
    
    def process_result(self, tag):
        
        data = {
            'entry': None,
            'cleaned_entry': None,
            'pos': None,
            'pronunciation': None,
            'alt_pronunciation': None,
            'html': None,
            'meanings': [],
            'deriatives': [],
        }
        
        if tag.get('id', None):
            data['entry'] = tag.get('id', None).strip()
            data['cleaned_entry'] = self.clean_accents(tag.get('id', None))
            data['html'] = str(tag)
        
        if tag.find(class_='pos').string:
            data['pos'] = tag.find(class_='pos').string.strip()
        
        if tag.find(class_='pronunciation'):
            data['pronunciation'] = self.process_pronunciation(
                tag=tag.find(class_='pronunciation'))
        
        if tag.find(class_='alternate-pronunciation'):
            data['alt_pronunciation'] = self.process_alt_pronunciation(
                tag=tag.find(class_='alternate-pronunciation'))
        
        # loop through all the senses
        # for sense in tag.find_all(class_='sense'):
        #     cleaned = self.process_sense(item=sense)
        #     if cleaned:
        #         data['meanings'].append(cleaned)
        
        # sense = tag.find_all(class_='sense')[0]
        # cleaned = self.process_sense(item=sense)
        # if cleaned:
        #     data['meanings'].append(cleaned)
        
        results = Word.objects().filter(entry=data.get('entry'))
        if not results:
            word = self.db.create_word(**data)
            return word
    
    def scrape_all(self, start: int = None, end: int = None,
                   from_letter: str = None, to_letter: str = None):
        
        msg = 'Fetching all words'
        if from_letter:
            msg += f' from {from_letter}'
        if to_letter:
            msg += f' up to {to_letter}'
        self.printer(f'{msg}...')
        
        qs = Letter.objects().all()
        if from_letter:
            qs = qs.filter(letter__gte=from_letter.upper())
        if to_letter:
            qs = qs.filter(letter__lte=to_letter.upper())
        
        for obj in qs:
            self.scrape_letter(obj.letter)
        
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
            
            for result in results:
                self.process_result(tag=result)
            
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
