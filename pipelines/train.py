# -*- coding: utf-8 -*-
import json

from werkzeug.exceptions import BadRequest

from .pipelineClient import init_pipeline_client
from .pipeline import Pipeline

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

    pipeline_runtime = run_details.pipeline_runtime
    run = run_details.run
    pipeline_spec = run.pipeline_spec
    resource_references = run.resource_references

    # format pipeline_runtime response
    resp_pipeline_runtime = {}
    resp_pipeline_runtime['pipeline_manifest'] = pipeline_runtime.pipeline_manifest
    resp_pipeline_runtime['workflow_manifest'] = json.loads(pipeline_runtime.workflow_manifest)

    # format run response
    resp_run = {}
    resp_run['id'] = run.id
    resp_run['name'] = run.name
    resp_run['created_at'] = run.created_at
    resp_run['finished_at'] = run.finished_at
    resp_run['description'] = run.description
    resp_run['error'] = run.error
    resp_run['status'] = run.status
    resp_run['metrics'] = run.metrics
    resp_run['scheduled_at'] = run.scheduled_at
    resp_run['storage_state'] = run.storage_state

    # format run pipeline spec response
    resp_pipeline_spec = {}
    resp_pipeline_spec['parameters'] = pipeline_spec.parameters
    resp_pipeline_spec['pipeline_id'] = pipeline_spec.pipeline_id
    resp_pipeline_spec['pipeline_manifest'] = pipeline_spec.pipeline_manifest
    resp_pipeline_spec['pipeline_name'] = pipeline_spec.pipeline_name
    resp_pipeline_spec['workflow_manifest'] = json.loads(pipeline_spec.workflow_manifest)
    resp_run['pipeline_spec'] = resp_pipeline_spec

    # format run resource references response
    resp_resource_references = []
    for references in resource_references:
        resource_references = {}
        resource_references['name'] = references.name
        resource_references['relationship'] = references.relationship
        key = {}
        key['id'] = references.key.id
        key['type'] = references.key.type
        resource_references['key'] = key
        resp_resource_references.append(resource_references)
    resp_run['resource_references'] = resp_resource_references
    
    # format run detail response
    resp_run_detail = {}
    resp_run_detail['pipeline_runtime'] = resp_pipeline_runtime
    resp_run_detail['run'] = resp_run
    return resp_run_detail