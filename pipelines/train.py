# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest

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
    