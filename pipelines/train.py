# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

from .pipeline import Pipeline
from .utils import validate_train_pipeline

def train_pipeline(request):
    req_data = request.get_json() or None

    try:
        # Validate request body schema
        if not validate_train_pipeline(req_data):
            raise BadRequest('Invalid request.')

        pipeline = Pipeline(
            req_data['experiment_id'],
            req_data['components'],
        )

        pipeline.set_input_files(
            req_data['csv'],
            req_data['txt']
        )

        pipeline.compile_train_pipeline()
        pipeline.run_pipeline()

        return {'message': 'Pipeline Running.'}

    except ValueError as err: 
        raise BadRequest('Invalid data: {}'.format(err))
    