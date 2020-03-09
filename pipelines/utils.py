# -*- coding: utf-8 -*-
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

def validate_parameters(parameters):
    try:
        for parameter in parameters:
            parameter_schema.validate(parameter)
        return True
    except SchemaError:
        return False

train_pipeline_schema = Schema({
    'experiment_id': str,
    'csv': str,
    'txt': str,
    'components': list
})

def validate_train_pipeline(pipeline):
    try:
        train_pipeline_schema.validate(pipeline)
        return True
    except SchemaError:
        return False

deploy_pipeline_schema = Schema({
    'experiment_id': str,
    'components': list
})

def validate_deploy_pipeline(pipeline):
    try:
        deploy_pipeline_schema.validate(pipeline)
        return True
    except SchemaError:
        return False
