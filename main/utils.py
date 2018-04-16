import os
import pprint

from simple_settings import LazySettings


class Printer(object):
    """
    A Borg Printer that only prints when --quiet is not True.
    
    TODO: refactor to have better templates.
    TODO: refactor to use multiple values in __call__.
    """
    
    __shared_state = {}  # Borg design pattern's shared state.
    
    def __init__(self, is_quiet=False, pretty=None, indent=1, noline=False,
                 prefix=None, *args, **kwargs):
        self.__dict__ = self.__shared_state
        self.is_quiet = is_quiet
        self.noline = noline
        self.prefix = prefix if prefix else '✨ '
        if not pretty:
            self.pretty = pprint.PrettyPrinter(indent=indent).pprint
        else:
            self.pretty = pretty
    
    def __call__(self, value=None, mode=None, header=False, footer=False,
                 endline=False, *args, **kwargs):
        if self.is_quiet:
            return
        
        if not value:  # default behavior when value is blank
            self.draw_line()
            return
        
        def print_text(with_prefix=False, *args_, **kwargs_):
            if with_prefix:
                print(self.prefix, end='')
            
            if not mode:
                print(value, *args_, **kwargs_)
            elif mode is 'pretty':
                self.pretty(value, *args_, **kwargs_)
        
        if header:
            print()
            self.add_format('BOLD')
            self.draw_line(char='%')
            print_text(with_prefix=True)
            self.draw_line(char='%')
            self.add_format('END')
            print()
        elif footer:
            print_text(with_prefix=True)
            self.draw_line()
        else:
            print_text()
        
        if endline:
            self.draw_line()
    
    def __str__(self):
        return f'Printer(is_quiet={self.is_quiet})'
    
    def draw_line(self, char=None, n=None):
        if self.noline:
            return
        char = char if char else '='
        n = n if n else os.get_terminal_size().columns
        print(char * n)
    
    def add_format(self, code, end=None):
        """
        Taken from https://stackoverflow.com/a/17303428
        """
        colors = {
            'PURPLE': '\033[95m',
            'CYAN': '\033[96m',
            'DARKCYAN': '\033[36m',
            'BLUE': '\033[94m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m',
            'END': '\033[0m',
        }
        end = end if end else ''
        print(colors.get(code), end=end)


def format_version(v):
    """
    Return a PEP 440-compliant version number from VERSION.
    
    Using "major.minor.micro" versioning.
    """
    
    version = f'{v[0]}.{v[1]}.{v[2]}'
    
    return version

def get_settings(filename=None):
    """
    Load settings from a file.
    """
    
    try:
        if not filename:
            raise NotImplementedError
        
        return LazySettings(filename)
    except NotImplementedError as e:
        sys.exit('No settings file provided.')
    except Exception as e:
        sys.exit('The application encountered an error during configuration.')

def create_using_template(template, base):
    """
    A little utility function that creates an object, and passes a Base.
    """
    
    def _create_using_template(*args, **kwargs):
        return template(base=base, *args, **kwargs)
    
    return _create_using_template
