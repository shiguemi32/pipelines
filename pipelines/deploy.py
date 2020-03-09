# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

from .pipeline import Pipeline
from .utils import validate_deploy_pipeline

def deploy_pipeline(request):
    req_data = request.get_json() or None

    try:
        if not validate_deploy_pipeline(req_data):
            raise BadRequest('Invalid request.')

        pipeline = Pipeline(
            req_data['experiment_id'],
            req_data['components']
        )

        pipeline.compile_deploy_pipeline()
        pipeline.upload_pipeline()

        return {'message': 'Pipeline successfully uploaded.'}

    except ValueError as err: 
        raise BadRequest('Invalid data: {}'.format(err))