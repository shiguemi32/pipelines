from textwrap import indent

class Component():
    def __init__(self, id, component_name, notebook_name):
        self.id = id
        self.component_name = component_name
        self.notebook_name = notebook_name
        self.dependencies = []

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def write_component(self):
        stmt = indent('''
notebook_path = \"s3://mlpipeline/{0}/{1}.ipynb\"
output_path = \"s3://mlpipeline/{{}}/{1}.ipynb\".format(experiment_id)
{0} = dsl.ContainerOp(
    name=\"{0}\",
    image=\"platiagro/autosklearn-notebook:latest\",
    
    command=[
        \"papermill\", notebook_path, output_path,
        \"-p\", \"bucket\", bucket,
        \"-p\", \"experiment_id\", experiment_id,
        \"-p\", \"workflow_name\", workflow_name,
        \"-p\", \"pod_name\", pod_name,
    ],
)'''.format(self.component_name, self.notebook_name), '    ')

        if self.dependencies:
            dependecies = str(", ".join(map(lambda d: d.component_name, self.dependencies)))
            stmt += ".after(" + dependecies + ")"

        return stmt

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_name: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_name, self.dependencies)
