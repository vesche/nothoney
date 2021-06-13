import json

modes = ['key', 'value']

class InvalidMode(Exception):
    pass

class ValidJsonPlox(Exception):
    pass

class ValidPathPlox(Exception):
    pass

def _omnomnom(obj, lookup, mode):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if mode == 'key' and lookup == key:
                yield value
            elif mode == 'value' and lookup == value:
                yield key
            yield from _omnomnom(value, lookup, mode)
    elif isinstance(obj, list):
        for item in obj:
            yield from _omnomnom(item, lookup, mode)

def eat(obj, lookup, mode='key', as_file=False):
    if mode not in modes:
        raise InvalidMode(f'Error! Mode must be one of: {modes}')
    if as_file:
        with open(obj) as f:
            try:
                obj = json.loads(f.read())
            except FileNotFoundError as e:
                raise ValidPathPlox(e)
            except json.decoder.JSONDecodeError as e:
                raise ValidJsonPlox(e)
    return [i for i in _omnomnom(obj, lookup, mode)]
