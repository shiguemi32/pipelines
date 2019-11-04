class Parameter():
    def __init__(self, name):
        self.name = name
    
    def read_parameter(self, parameter):
        self.value = parameter.get('value')
        self.type = parameter.get('type')
        self.default = parameter.get('default')

    def write_parameter(self):
        stmt = ""

        if self.value != None:
            stmt = '\"-p\", \"{}\", {},'.format(self.name, repr(self.value))
        elif self.type != None:
            stmt = '\"-p\", \"{0}\", {0},'.format(self.name)

        return stmt

