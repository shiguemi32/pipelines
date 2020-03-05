# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

def deploy_pipeline(request):
    req_data = request.get_json() or None

    try:
        return {'message': 'Pipeline successfully deployed.'}

    except ValueError as err: 
        raise BadRequest('Invalid data: {}'.format(err))

    except SchemaMissingKeyError as err:
        raise BadRequest(err)
