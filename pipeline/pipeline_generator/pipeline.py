import requests
import os
from collections import defaultdict
from uuid import uuid4
from .utils import write_on_boilerplate

class Pipeline():
    ''' Implementing a basic graph structure for pipelines. '''

    def __init__(self, components, edges):
        self.components = components
        self.adj = defaultdict(set)
        self.add_edges(edges)

    def add_edges(self, edges):
        for u, v in edges:
            self.adj[u].add(v)

    def execute_script(self):
        cwd = os.path.join(os.getcwd(), "pipelines_scripts/{}.py".format(self.pipeline_id))

        os.system('{} {}'.format('python', cwd))

    def get_parameters(self):
        stmt = ''
        parameters = []

        for c in self.components.values():
            for p in c.parameters:
                if p.type != None and not p.name in parameters:
                    stmt += '{}: {} = {},\n'.format(p.name, p.type, repr(p.default))
                    parameters.append(p.name)

        return stmt[:-2]

    def upload_pipeline(self):
        url = 'http://127.0.0.1:31380/pipeline/apis/v1beta1/pipelines/upload?name={}'.format(self.pipeline_id)

        path = 'pipelines_scripts/{}.py.zip'.format(self.pipeline_id)
        files = {'uploadfile': open(path, 'rb')}

        try:
            r = requests.post(url, files=files)
        except requests.exceptions.RequestException as err:
            print(err)
            raise Exception('Failed to connect to Kubeflow Pipelines API.')

    def write_script(self):
        self.pipeline_id = uuid4()

        roots = [component.id for component in self.components.values() 
                 if not component.dependencies]

        components_objects = dict.copy(self.components)

        components_str = []

        def verify_level(level, components):
            if len(components) == 0:
                return True
            for i in level:
                if write_component(i, components_objects):
                    components_objects.pop(i, None)
                    if verify_level(self.adj[i], components_objects):
                        return True
            return False

        def write_component(node, components):
            for d in components_objects[node].dependencies:
                if d.id in components.keys():
                    return False
            components_str.append(components_objects[node].write_component())

            return True

        verify_level(roots, components_objects)

        components_code = ''.join(components_str)

        parameters = self.get_parameters()

        stmt = write_on_boilerplate(components_code, parameters)

        path = 'pipelines_scripts/{}.py'.format(self.pipeline_id)

        os.makedirs("pipelines_scripts", exist_ok=True)
        with open(path, 'w') as file_object:
            file_object.write(stmt)
        
    def __len__(self):
        return len(self.adj)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))

    def __getitem__(self, v):
        return self.adj[v]
