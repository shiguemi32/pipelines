from textwrap import indent

class Component():
    def __init__(self, id, component_name, notebook_name, image):
        self.id = id
        self.component_name = component_name
        self.notebook_name = notebook_name
        self.image = image
        self.dependencies = []
        self.parameters = []

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def write_component(self):
        parameters = str('\n'.join([p.write_parameter() for p in self.parameters]))    

        stmt = indent('''
notebook_path = \"s3://mlpipeline/{0}/{1}.ipynb\"
output_path = \"s3://mlpipeline/{{}}/{1}.ipynb\".format(experiment_id)
{0} = dsl.ContainerOp(
    name=\"{0}\",
    image=\"{2}\",
    container_kwargs={{\"image_pull_policy\": \"IfNotPresent\"}},
    command=[
        \"papermill\", notebook_path, output_path,
        \"-p\", \"bucket\", bucket,
        \"-p\", \"experiment_id\", experiment_id,
        \"-p\", \"workflow_name\", workflow_name,
        \"-p\", \"pod_name\", pod_name,
{3}
    ],
)'''.format(self.component_name, self.notebook_name, 
            self.image, indent(parameters, '        ')), '    ')

        if self.dependencies:
            dependecies = str(", ".join([d.component_name for d in self.dependencies]))
            stmt += ".after(" + dependecies + ")"

        return stmt

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_name: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_name, self.dependencies)
