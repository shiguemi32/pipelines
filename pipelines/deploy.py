# -*- coding: utf-8 -*-
import json

from werkzeug.exceptions import BadRequest
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from .pipeline import Pipeline
from .utils import init_pipeline_client


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
    res = []

    client = init_pipeline_client()

    list_runs = client.list_runs(sort_by='created_at').runs

    import socket
    ip = socket.gethostbyname(socket.gethostname())

    for run in list_runs:
        manifest = run.pipeline_spec.workflow_manifest
        if 'SeldonDeployment' in manifest:
            res.append({
                'uuid': run.name,
                'status': run.status,
                'url':
                    'http://{}/seldon/anonymous/{}/api/v1.0/predictions'.format(
                        ip, 'deploy-' + run.name) if run.status == 'Succeeded' else None,
                'createdAt': run.created_at
            })

    return res


def get_deployment_log(pod, container):
    """Get logs from deployment.

    Args:
        pod (str): pod name.
        container (str): container name.
    """
    if not pod:
        raise BadRequest('Missing the parameter: pod')

    if not container:
        raise BadRequest('Missing the parameter: container')

    config.load_incluster_config()
    v1 = client.CoreV1Api()
    try:
        namespace = 'anonymous'

        # get full pod name
        pods = v1.list_namespaced_pod(namespace)
        for i in pods.items:
            pod_name = i.metadata.name
            if pod_name.startswith(pod):
                pod = pod_name
                break

        return v1.read_namespaced_pod_log(pod, namespace, container=container, pretty='true', tail_lines=512, timestamps=True)
    except ApiException as e:
        body = json.loads(e.body)
        error_message = body['message']
        raise BadRequest('{}'.format(error_message))
