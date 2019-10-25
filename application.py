from os import getenv
from os.path import dirname, isfile, join
from dotenv import load_dotenv

from pipeline import create_app

_ENV_FILE = join(dirname(__file__), '.env')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

app = create_app(getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    IP = '0.0.0.0'
    PORT = app.config['APP_PORT']
    DEBUG = app.config['DEBUG']

    app.run(
        host=IP, debug=DEBUG, port=PORT
    )
