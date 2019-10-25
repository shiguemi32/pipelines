# -*- coding: utf-8 -*-
'''
App main package
'''
from flask import Flask

from config import config
from .api import configure_api

def create_app(config_name):
    app = Flask('pipeline-api')

    app.config.from_object(config[config_name])

    configure_api(app)

    return app


__version__ = "0.1.0"
