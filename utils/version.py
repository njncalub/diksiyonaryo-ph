def format_version(v):
    """
    Return a PEP 440-compliant version number from VERSION.
    
    Using "major.minor.micro" versioning.
    """
    
    version = f'{v[0]}.{v[1]}.{v[2]}'
    
    return version
