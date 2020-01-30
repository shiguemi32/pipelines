from re import sub

from unicodedata import normalize

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