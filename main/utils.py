def get_version(ver):
    """
    Return a PEP 440-compliant version number from VERSION.
    
    Using "major.minor.micro" versioning.
    """
    
    version = f'{ver[0]}.{ver[1]}.{ver[2]}'
    
    return version

def init_database():
    """
    Initialize the database.
    """
    pass
