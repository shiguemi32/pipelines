import kfp
import kfp.compiler as compiler
import kfp.dsl as dsl

from .utils import normalize_string
from .component import Component

class Pipeline():
    def __init__(self, components):
        self.components = self._init_components(components)
        self._get_dependencies(components)

        self.client = self._init_client()
        
        EXPERIMENT_NAME = 'Teste'
        experiment = self.client.create_experiment(name=EXPERIMENT_NAME)

        self.experiment = experiment

    def _init_client(self):
        return kfp.Client('0.0.0.0:31380/pipeline')

    def _init_components(self, components):
        components_objects = []

        for index, component in enumerate(components):
            try:
                component_name = normalize_string(component['component_name'])
                notebook_path = component['notebook_path']
            except KeyError:
                raise ValueError('Invalid component.')

            components_objects.append(
                Component(index, component_name, notebook_path))

        return components_objects

    def _search_dependency(self, dependency):
        for component in self.components:
            if component.component_name == dependency:
                return component
        raise ValueError('Invalid dependency')

    def _get_dependencies(self, components):
        for index, component in enumerate(components):
            component_object = self.components[index]
            try:    
                dependencies = component['dependencies']
                for dependency in dependencies:
                    dependency_name = normalize_string(dependency)

                    if dependency_name == component_object.component_name:
                        raise ValueError('Self-dependent.')

                    component_object.add_dependency(self._search_dependency(dependency_name))

            except KeyError:
                continue

    def compile_pipeline(self):
        @dsl.pipeline(name='Common pipeline')
        def pipeline():
            for component in self.components:
                component.create_container_op()

            for component in self.components:
                if component.dependencies:
                    component.container_op.after(
                        *[dependency.container_op 
                            for dependency in component.dependencies
                            ])

        compiler.Compiler().compile(pipeline, 'result.tar.gz')

    def run_pipeline(self):
        run = self.client.run_pipeline(self.experiment.id, 'result',
                                       'result.tar.gz')
