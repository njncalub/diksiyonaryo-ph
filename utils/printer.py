import os
import pprint

from colorama import Fore


class Printer(object):
    """
    A Borg Printer that only prints when --quiet is False.
    """
    
    __shared_state = {}
    __instantiated = False
    
    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state
        
        # exit if already instantiated
        if self.__instantiated:
            return
        else:
            self.__instantiated = True
        
        options = {
            'is_quiet': False,
            'no_line': False,
            'line_char': '%',
            'prefix': '✨ ',
            'indent': 1,
        }
        options.update(kwargs)
        
        for key in options:
            self.__setattr__(key, options[key])
        
        self.pretty = pprint.PrettyPrinter(indent=self.indent).pprint
    
    def __call__(self, value, *args, **kwargs):
        if self.is_quiet:
            return
        
        msg_type = kwargs.pop('msg_type', None)
        if msg_type == 'header':
            self.header_msg(value=value, *args, **kwargs)
        elif msg_type == 'error':
            self.error_msg(value=value, *args, **kwargs)
        elif msg_type == 'success':
            self.success_msg(value=value, *args, **kwargs)
        else:
            self.print_text(value, *args, **kwargs)
    
    def __str__(self):
        return f'Printer(is_quiet={self.is_quiet})'
    
    def print_text(self, value, *args, **kwargs):
        if self.is_quiet:
            return
        
        mode = kwargs.pop('mode', None)
        if not mode:
            print(value, *args, **kwargs)
        elif mode == 'pretty':
            self.pretty(value, *args, **kwargs)
    
    def header_msg(self, value, *args, **kwargs):
        if self.is_quiet:
            return
        
        style = kwargs.pop('style', None)
        
        self.draw_line(line_char='%', prefix='\033[1m', style=style)
        
        if style == 'success':
            self.success_msg(value=value, *args, **kwargs)
        elif style == 'error':
            self.error_msg(value=value, *args, **kwargs)
        else:
            self.print_text(value=value, *args, **kwargs)
        
        self.draw_line(line_char='%', prefix='\033[1m', style=style)
    
    def success_msg(self, value, *args, **kwargs):
        if self.is_quiet:
            return
        
        self.print_text(Fore.LIGHTGREEN_EX + value + Fore.WHITE, *args,
                        **kwargs)
    
    def error_msg(self, value, *args, **kwargs):
        if self.is_quiet:
            return
        
        self.print_text(Fore.LIGHTRED_EX + value + Fore.WHITE, *args, **kwargs)
    
    def draw_line(self, prefix: str = None, line_char: str = None,
                  width: int = None, style: str = None, *args, **kwargs):
        if self.no_line:
            return
        
        prefix = prefix if prefix else ''
        line_char = line_char if line_char else self.line_char
        width = width if width else os.get_terminal_size().columns
        text = self.line_char * width
        
        if style == 'success':
            text = Fore.LIGHTGREEN_EX + text + Fore.WHITE
        elif style == 'error':
            text = Fore.LIGHTRED_EX + text + Fore.WHITE
        
        if prefix:
            text = prefix + text
        
        print(text)


def init_printer(is_quiet):
    return Printer(is_quiet=is_quiet)
