from services.scraper import Scraper


def init_scraper_service(base_url=None, next_button_text=None,
                         letter_list_uri=None, letter_list_page_uri=None,
                         result_item_selector=None, printer=None, db=None,
                         *args, **kwargs) -> Scraper:
    options = {
        'base_url': base_url,
        'next_button_text': next_button_text,
        'letter_list_uri': letter_list_uri,
        'letter_list_page_uri': letter_list_page_uri,
        'result_item_selector': result_item_selector,
        'printer': printer,
        'db': db,
    }
    
    return Scraper(**options)
