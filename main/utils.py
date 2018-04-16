from .models import Base, Connection


def format_version(v):
    """
    Return a PEP 440-compliant version number from VERSION.
    
    Using "major.minor.micro" versioning.
    """
    
    version = f'{v[0]}.{v[1]}.{v[2]}'
    
    return version

def create_using_template(template, base):
    """
    A little utility function that creates an object, and passes a Base.
    """
    
    def _create_using_template(*args, **kwargs):
        return template(base=base, *args, **kwargs)
    
    return _create_using_template

get_or_create_connection = create_using_template(template=Connection, base=Base)
