# -*- coding: utf-8 -*-
from schema import Schema, And, SchemaMissingKeyError
from werkzeug.exceptions import BadRequest

from .pipeline import Pipeline

train_pipeline_schema = Schema({
    'experiment_id': And(str),
    'csv': And(str),
    'txt': And(str),
    'components': And(list)
    })

def train_pipeline(request):
    req_data = request.get_json() or None

    try:
        # Validate request body schema
        train_pipeline_schema.validate(req_data)

        pipeline = Pipeline(
            req_data['experiment_id'],
            req_data['components'],
            req_data['csv'],
            req_data['txt']
        )

        pipeline.compile_train_pipeline()
        pipeline.run_pipeline()

        return {'message': 'Pipeline Running.'}

    except ValueError as err: 
        raise BadRequest('Invalid data: {}'.format(err))

    except SchemaMissingKeyError as err:
        raise BadRequest(err)
    