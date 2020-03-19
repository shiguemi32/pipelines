# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

from .pipelineClient import init_pipeline_client
from .pipeline import Pipeline
from .utils import format_pipeline_run

def deploy_pipeline(pipeline_parameters):
    """Compile and run a deployment pipeline.

    Args:
        pipeline_parameters (dict): request body json, format:
            experiment_id (str): PlatIAgro experiment's uuid.
            components (list): list of pipeline components.
            dataset (str): dataset id.
            target (str): target column from dataset.
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

    pipeline = Pipeline(experiment_id, components)

    pipeline.compile_deploy_pipeline()
    
    pipeline.upload_pipeline()

def get_deploys():
    """Get deploy list.

    Returns:
        Deploy list.
    """
    client = init_pipeline_client()
    runs = []
    token = ''
    while True:
        list_runs = client.list_runs(page_token=token, sort_by='created_at desc',page_size=20)
        if list_runs.runs is not None:
            for run in list_runs.runs:
                _run = format_pipeline_run(run)
                runs.append(_run)
            token = list_runs.next_page_token
            runs_size = len(list_runs.runs)
            if runs_size == 0 or token is None:
                break
        else:
            break
    return {'runs': runs}