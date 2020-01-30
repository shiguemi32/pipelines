import kfp
import kfp.compiler as compiler
import kfp.dsl as dsl


class Pipeline():
    def __init__(self, components):
        self.components = components

        client = kfp.Client('0.0.0.0:31380/pipeline')
        EXPERIMENT_NAME = 'Teste'
        experiment = client.create_experiment(name=EXPERIMENT_NAME)

        self.client = client
        self.experiment = experiment

    def compile_pipeline(self):
        @dsl.pipeline(name='Common pipeline')
        def run_workflow():
            for c in self.components:
                c.write_component()

        compiler.Compiler().compile(run_workflow, 'result.tar.gz')

    def run_pipeline(self):
        run = self.client.run_pipeline(self.experiment.id, 'result',
                                       'result.tar.gz')
