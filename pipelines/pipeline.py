# -*- coding: utf-8 -*-
import json

from kfp import compiler, dsl
from werkzeug.exceptions import BadRequest

from .utils import init_pipeline_client, validate_component, validate_parameters
from .resources.templates import SELDON_DEPLOYMENT
from .component import Component


class Pipeline():
    """Represents a KubeFlow Pipeline.

    Train or deploy in KubeFlow the given pipeline.
    """

    def __init__(self, experiment_id, components, dataset, target):
        """Create a new instance of Pipeline.

        Args:
            experiment_id (str): PlatIAgro experiment's uuid.
            components (list): list of pipeline components.
            dataset (str): dataset id.
            target (str): target column from dataset.
        """
        # Instantiate pipeline's components
        self._experiment_id = experiment_id
        self._dataset = dataset
        self._target = target

        self._first = self._init_components(components)

        self._client = init_pipeline_client()
        self._experiment = self._client.create_experiment(name=experiment_id)

    def _init_components(self, raw_components):
        """Instantiate the given components.

        Args:
            raw_components (list): list of component objects.

        Component objects format:
            operator_id (str): PlatIA operator UUID.
            notebook_path (str): component notebook MinIO path.
            parameters (list): component parameters list. (optional)

        Returns:
            The first component from this pipeline.
        """
        previous = None

        for index, component in enumerate(raw_components):
            # check if component are in the correct format
            if not validate_component(component):
                raise BadRequest('Invalid component in request.')

            operator_id = component.get('operatorId')
            notebook_path = component.get('notebookPath')

            parameters = component.get('parameters', None)
            # validate parameters
            if parameters:
                if not validate_parameters(parameters):
                    raise ValueError('Invalid parameter.')

            if index == 0:
                # store the first component from pipeline
                first = Component(self._experiment_id, self._dataset, self._target,
                                  operator_id, notebook_path, parameters, None)
                previous = first
            else:
                current_component = Component(
                    self._experiment_id, self._dataset, self._target, operator_id, notebook_path, parameters, previous)
                previous.set_next_component(current_component)
                previous = current_component

        return first

    def _create_component_specs_json(self):
        """Create KubeFlow specs to each component from this pipeline.

        Returns:
            A string in JSON format with the specs of each component.
        """
        specs = []
        component = self._first

        while component:
            specs.append(component.create_component_spec())
            component = component.next

        return ",".join(specs)

    def _create_graph_json(self):
        """Create a KubeFlow Graph in JSON format from this pipeline.

        Returns:
            A string in JSON format describing this pipeline.
        """
        return self._first.create_component_graph()

    def compile_train_pipeline(self):
        """Compile the pipeline in a train format."""
        @dsl.pipeline(name='Common pipeline')
        def train_pipeline():
            prev = None
            component = self._first

            while component:
                component.create_container_op()

                if prev:
                    component.container_op.after(prev.container_op)

                prev = component
                component = component.next

        compiler.Compiler().compile(train_pipeline, self._experiment_id + '.tar.gz')

    def compile_deploy_pipeline(self):
        """Compile pipeline in a deploy format."""
        component_specs = self._create_component_specs_json()
        graph = self._create_graph_json()

        @dsl.pipeline(name='Common Seldon Deployment.')
        def deploy_pipeline():
            seldonserving = SELDON_DEPLOYMENT.substitute({
                "namespace": "anonymous",
                "experimentId": self._experiment_id,
                "componentSpecs": component_specs,
                "graph": graph
            })

            seldon_deployment = json.loads(seldonserving)
            serve_op = dsl.ResourceOp(
                name="deploy",
                k8s_resource=seldon_deployment,
                success_condition="status.state == Available"
            ).set_timeout(300)

            component = self._first
            while component:
                component.build_component()
                serve_op.after(component.build)
                component = component.next

        compiler.Compiler().compile(deploy_pipeline, self._experiment_id + '.tar.gz')

    def run_pipeline(self):
        """Run this pipeline on the KubeFlow instance. 

        Returns:
            KubeFlow run object.
        """
        run = self._client.run_pipeline(self._experiment.id, self._experiment_id,
                                        self._experiment_id + '.tar.gz')

        return run.id
