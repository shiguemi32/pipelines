import kfp
import kfp.compiler as compiler
import kfp.dsl as dsl

from .utils import normalize_string, validate_parameter
from .component import Component

class Pipeline():
    def __init__(self, experiment_id, components, csv, txt):
        self.csv = csv
        self.txt = txt

        self.components = self._init_components(components)

        self.client = self._init_client()
        
        experiment = self.client.create_experiment(name=experiment_id)

        self.experiment = experiment

    def _init_client(self):
        return kfp.Client('0.0.0.0:31380/pipeline')

    def _init_components(self, components):
        components_objects = []

        for i, component in enumerate(components):
            try:
                component_name = normalize_string(component['component_name'])
                notebook_path = component['notebook_path']

                prev = components_objects[i - 1] if i != 0 else None

                parameters = component.get('parameters', None)
                
                # Validate parameters
                if parameters:
                    for p in parameters:
                        if not validate_parameter(p):
                            raise ValueError('Invalid parameter.')

                component_object = Component(
                    i, 
                    component_name,
                    notebook_path,
                    parameters)

                components_objects.append(component_object)

                if prev:
                    component_object.set_input_files(prev.out_csv, prev.out_txt)
                else:
                    component_object.set_input_files(self.csv, self.txt)

            except KeyError:
                raise ValueError('Invalid component.')

        return components_objects

    def compile_pipeline(self):
        @dsl.pipeline(name='Common pipeline')
        def pipeline():
            for index, component in enumerate(self.components):
                component.create_container_op()
                
                if index != 0:
                    prev = self.components[index - 1]
                    component.container_op.after(prev.container_op)

        compiler.Compiler().compile(pipeline, 'result.tar.gz')

    def run_pipeline(self):
        run = self.client.run_pipeline(self.experiment.id, 'result',
                                       'result.tar.gz')