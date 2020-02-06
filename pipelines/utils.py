from re import sub

from unicodedata import normalize
from schema import Schema, SchemaError, Use, Or, Optional

def normalize_string(string):
    # Normalize string
    normalized = (normalize("NFD", string)
                  .encode("ascii", "ignore")
                  .decode("utf-8")
                  .lower())

    # Remove invalid chars
    normalized = sub(r'([^\w\s]|_)+(?=\s|$)', '', normalized)
    normalized = sub('[^A-Za-z0-9]+', '_', normalized)

    return normalized

parameter_schema = Schema({
    'name': str,
    'type': str,
    'value': Or(str, int, float),
    Optional('description'): str
})

def validate_parameter(parameter):
    try:
        parameter_schema.validate(parameter)
        return True
    except SchemaError as err:
        return False