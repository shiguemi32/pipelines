class Parameter():
    def __init__(self, name, value, type, default):
        self.name = name
        self.value = value
        self.type = type
        self.default = default
    
    @staticmethod
    def read_parameter(parameter):
        name = parameter.get('name')
        value = parameter.get('value')
        type = parameter.get('type')
        default = parameter.get('default')

        return Parameter(name, value, type, default)

    def write_parameter(self):
        stmt = ""

        if self.value != None:
            stmt = '\"-p\", \"{}\", {},'.format(self.name, repr(self.value))
        elif self.type != None:
            stmt = '\"-p\", \"{0}\", {0},'.format(self.name)

        return stmt

