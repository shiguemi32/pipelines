# -*- coding: utf-8 -*-
import json

from werkzeug.exceptions import BadRequest
from kubernetes import client, config
from kubernetes.client import Configuration, ApiClient
from kubernetes.client.rest import ApiException

from .pipeline import Pipeline
from .utils import init_pipeline_client, format_pipeline_run


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
        experiment_id = pipeline_parameters['experimentId']
        components = pipeline_parameters['components']
        dataset = pipeline_parameters['dataset']
        target = pipeline_parameters['target']
    except KeyError as e:
        raise BadRequest(
            'Invalid request body, missing the parameter: {}'.format(e)
        )

    pipeline = Pipeline(experiment_id, components, dataset, target)
    pipeline.compile_deploy_pipeline()
    return pipeline.run_pipeline()


def get_deploys():
    """Get deploy list.

    Returns:
        Deploy list.
    """
    client = init_pipeline_client()
    runs = []
    token = ''
    while True:
        list_runs = client.list_runs(
            page_token=token, sort_by='created_at desc', page_size=100)
        if list_runs.runs is not None:
            for run in list_runs.runs:
                # check if run is type deployment
                manifest = run.pipeline_spec.workflow_manifest
                if 'SeldonDeployment' in manifest:
                    _run = format_pipeline_run(run)
                    runs.append(_run)
            token = list_runs.next_page_token
            runs_size = len(list_runs.runs)
            if runs_size == 0 or token is None:
                break
        else:
            break
    return {'runs': runs}


def get_deployment_log(parameters):
    """Get logs from deployment.

    Args:
        parameters (dict): request body json, format:
            pod (str): pod name.
            container (str): container name.
    """
    try:
        pod = parameters['pod']
        container = parameters['container']
    except KeyError as e:
        raise BadRequest(
            'Invalid request body, missing the parameter: {}'.format(e)
        )

    config.load_incluster_config()
    v1 = client.CoreV1Api()
    try:
        return v1.read_namespaced_pod_log(pod, 'anonymous', container=container, pretty='true', tail_lines=512, timestamps=True)
    except ApiException as e:
        body = json.loads(e.body)
        error_message = body['message']
        raise BadRequest('{}'.format(error_message))
    