# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

from .pipelineClient import init_pipeline_client
from .pipeline import Pipeline
from .utils import format_pipeline_run_details

def train_pipeline(pipeline_parameters):
    """Compile and run a train pipeline.

    Args:
        pipeline_parameters (dict): request body json, format:
            experiment_id (str): PlatIAgro experiment's uuid.
            components (list): list of pipeline components.
            dataset (str): dataset id.
            target (str): target column from dataset.

    Returns:
        Pipeline run id.
    """
    try:
        experiment_id = pipeline_parameters['experiment_id']
        components = pipeline_parameters['components']
        dataset = pipeline_parameters['dataset']
        target = pipeline_parameters['target']
    except KeyError as e:
        raise BadRequest(
            'Invalid request body, missing the parameter: {}'.format(e)
        )

    pipeline = Pipeline(experiment_id, components, dataset, target)

    pipeline.compile_train_pipeline()

    return pipeline.run_pipeline()


def train_pipeline_status(run_id):
    """Get run details.

    Args:
        run_id (str): experiment run id.

    Returns:
       Run details.
    """
    run_details = ''
    try:
        client = init_pipeline_client()
        run_details = client.get_run(run_id)
    except Exception:
        raise BadRequest('Not found run with id: {}'.format(run_id))

    return format_pipeline_run_details(run_details)