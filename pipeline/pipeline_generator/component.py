class Component():
    def __init__(self, id, component_name, notebook_name):
        self.id = id
        self.component_name = component_name
        self.notebook_name = notebook_name
        self.dependencies = []

    def add_dependence(self, dependence):
        self.dependencies.append(dependence)

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_name: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_name, self.dependencies)
