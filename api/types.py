from apistar import exceptions, types, validators


class Word(types.Type):
    entry = validators.String(max_length=100)
    cleaned_entry = validators.String(max_length=100)
    html = validators.String()
