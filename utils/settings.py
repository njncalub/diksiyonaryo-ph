import sys

from simple_settings import LazySettings


class ProjectSettings(object):
    """
    A Borg ProjectSettings object that you only need to instantiate once.
    """
    
    __shared_state = {}  # Borg design pattern's shared state.
    
    def __init__(self, filename=None, *args, **kwargs):
        self.__dict__ = self.__shared_state
        
        try:
            # check if object was already instantiated
            if self.__dict__.get('filename') and self.__dict__.get('config'):
                return
            
            if filename:
                self.filename = filename
                self.config = LazySettings(self.filename)
            else:
                raise NotImplementedError
        except NotImplementedError as e:
            print('Please pass a filename first.')
            print(sys.exc_info())
        except Exception as e:
            print(sys.exc_info())
    
    def __getattr__(self, key):
        """
        Called if there is no class attribute found on the object.
        """
        try:
            if self.config:
                return self.config.as_dict().get(key)
            else:
                raise NotImplementedError
        except NotImplementedError as e:
            print('LazySettings not yet created.')
            print(sys.exc_info())
        except Exception as e:
            print(sys.exc_info())
    
    def __str__(self):
        return f'ProjectSettings(filename={self.filename})'
    
    def as_dict(self):
        if self.config:
            return self.config.as_dict()
        else:
            return {}


def load_settings(filename):
    return ProjectSettings(filename=filename)
