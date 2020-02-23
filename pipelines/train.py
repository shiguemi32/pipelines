from schema import Schema, And, SchemaMissingKeyError
from werkzeug.exceptions import BadRequest

from .pipeline import Pipeline

create_train_pipeline_schema = Schema({
    'experiment_id': And(str),
    'csv': And(str),
    'txt': And(str),
    'components': And(list)
    })

def create_train_pipeline(request):
    req_data = request.get_json() or None

    try:
        # Validate request body schema
        create_train_pipeline_schema.validate(req_data)

        components = req_data.get('components', None)
        experiment_id = req_data.get('experiment_id', None)
        csv = req_data.get('csv', None)
        txt = req_data.get('txt', None)

        pipeline = Pipeline(experiment_id, components, csv, txt)

        pipeline.compile_pipeline()
        pipeline.run_pipeline()

        return {'message': 'Pipeline Running.'}

    except ValueError as err: 
        raise BadRequest('Invalid data: {}'.format(err))

    except SchemaMissingKeyError as err:
        raise BadRequest(err)
    