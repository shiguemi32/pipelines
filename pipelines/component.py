# -*- coding: utf-8 -*-
import os
import yaml

from kfp import components, dsl
from kubernetes import client as k8s_client

from .utils import init_pipeline_client, validate_notebook_path
from .resources.templates import PAPERMILL_YAML, COMPONENT_SPEC, GRAPH


class Component():
    """Represents a Pipeline Component.

    Attributes:
        container_op (kfp.dsl.ContainerOp): component operator.
    """

    def __init__(self, experiment_id, operator_id, notebook_path, parameters, prev):
        """Create a new instance of Component.

        Args:
            operator_id (str): PlatIA operator UUID.
            notebook_path (str): path to component notebook in MinIO.
            parameters (list): list of component parameters.
            prev (Component): previous component in pipeline.
        """
        self._experiment_id = experiment_id
        self._operator_id = operator_id
        self._notebook_path = validate_notebook_path(notebook_path)

        self._parameters = parameters
        self.container_op = None

        self._image = 'miguelfferraz/platia-{}:latest'.format(
            self._operator_id)

        self.next = None
        self.prev = prev

        self.set_output_file()

    def _create_parameters_papermill(self):
        if self._parameters:
            parameters_string = []

            for parameter in self._parameters:
                parameters_string.append('-p ' + parameter['name'] + ' '
                                         + parameter['value'] + ',')

            return ' '.join(parameters_string)
        return ''

    def _create_component_yaml(self):
        yaml_template = yaml.load(PAPERMILL_YAML.substitute({
            "operatorName": "PlatIA-" + self._operator_id,
            "parameters": self._create_parameters_papermill()
        }), Loader=yaml.FullLoader)

        file_name = '{}.yaml'.format(self._operator_id)
        file_path = os.path.join(os.path.dirname(
            __file__), 'resources', file_name)

        with open(file_path, 'w') as f:
            yaml.dump(yaml_template, f)

        return file_path

    def create_component_spec(self):
        """Create a string from component spec.

        Returns:
            Component spec in JSON format."""

        component_spec = COMPONENT_SPEC.substitute({
            "image": self._image,
            "name": self._operator_id,
            "parameters": self._parameters if self._parameters else '[{}]'
        })

        return component_spec

    def create_component_graph(self):
        """Recursively creates a string from the component's graph
        with its children.

        Returns:
            Pipeline components graph in JSON format.
        """
        component_graph = GRAPH.substitute({
            "name": self._operator_id,
            "type": "TRANSFORMER" if self.next else "MODEL",
            "children": self.next.create_component_graph() if self.next else ""
        })

        return component_graph

    def create_container_op(self):
        """Create component operator from YAML file."""
        notebook_path = self._notebook_path
        output_path = self._notebook_path + ".out"

        fpath = self._create_component_yaml()
        container = components.load_component_from_file(fpath)

        self.container_op = container(
            notebook_path=notebook_path,
            output_path=output_path,
            experiment_id=self._experiment_id,
            dataset=self.dataset,
            target=self.target,
            out_dataset=self.out_dataset).set_image_pull_policy('Always')

    def build_component(self, dataset, target):
        image_name = self._image
        notebook_path = self._notebook_path

        secret = k8s_client.V1Volume(
            name='docker-config-secret',
            secret=k8s_client.V1SecretVolumeSource(secret_name='docker-config')
        )
        wkdirop = dsl.VolumeOp(
            name='wkdirpvc' + self._operator_id,
            resource_name='wkdirpvc' + self._operator_id,
            size='50Mi',
            modes=dsl.VOLUME_MODE_RWO
        )
        export_notebook = dsl.ContainerOp(
            name='export-notebook',
            # TODO: Change to PlatIAgro datascience image
            image='miguelfferraz/datascience-image',
            command=['sh', '-c'],
            arguments=[
                'papermill {} - --log-level DEBUG'.format(notebook_path)],
            pvolumes={'/home/jovyan': wkdirop.volume}
        )
        export_notebook.container.add_env_variable(k8s_client.V1EnvVar(name='EXPERIMENT_ID', value=self._experiment_id)).add_env_variable(
            k8s_client.V1EnvVar(name='DATASET', value=dataset)).add_env_variable(k8s_client.V1EnvVar(name='TARGET', value=target))
        clone = dsl.ContainerOp(
            name='clone',
            image='alpine/git:latest',
            command=['sh', '-c'],
            # TODO: Change git repo to upstream master
            arguments=['git clone --depth 1 --branch feature/build-component-image https://github.com/miguelfferraz/pipelines; cp ./pipelines/pipelines/resources/image_builder/* /workspace;'],
            pvolumes={'/workspace': export_notebook.pvolume}
        )
        build = dsl.ContainerOp(
            name='build',
            image='gcr.io/kaniko-project/executor:debug',
            arguments=['--dockerfile', 'Dockerfile', '--context',
                       'dir://workspace', '--destination', image_name],
            pvolumes={'/workspace': clone.pvolume, '/root/.docker/': secret}
        )

        self.build = build

    def set_next_component(self, next_component):
        self.next = next_component

    def set_input_file(self, dataset, target):
        self.dataset = dataset
        self.target = target

    def set_output_file(self):
        self.out_dataset = self._operator_id + '.csv'
