from textwrap import indent

from .parameter import Parameter

class Component():
    def __init__(self, id, component_name, notebook_path, image):
        self.id = id
        self.component_name = component_name
        self.notebook_path = notebook_path
        self.image = image
        self.dependencies = []
        self.parameters = []

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def add_parameter(self, parameter_properties):
        parameter = Parameter.read_parameter(parameter_properties)
        self.parameters.append(parameter)

    def write_component(self):
        parameters = str('\n'.join([p.write_parameter() for p in self.parameters]))   

        output_path = self.notebook_path.split('/')
        del output_path[-2]
        output_path[-2] = '{}'
        output_path = '/'.join(output_path) 

        stmt = indent('''
notebook_path = \"{1}\"
output_path = \"{4}\".format(experiment_id)
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
)'''.format(self.component_name, self.notebook_path, 
            self.image, indent(parameters, '        '),
            output_path), '    ')

        if self.dependencies:
            dependecies = str(", ".join([d.component_name for d in self.dependencies]))
            stmt += ".after(" + dependecies + ")"

        return stmt

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_name: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_name, self.dependencies)
