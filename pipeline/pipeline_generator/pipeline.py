from collections import defaultdict

class Pipeline():
    ''' Implementing a basic graph structure for pipelines. '''

    def __init__(self, components, edges):
        self.components = components
        self.adj = defaultdict(set)
        self.add_edges(edges)

    def add_edges(self, edges):
        for u, v in edges:
            self.adj[u].add(v)

    def write_script(self):
        roots = [component.id for component in self.components.values() 
                 if not component.dependencies]

        components = self.components   

        def verify_level(level, components):
            if len(components) == 0:
                return True
            for i in level:
                if write_component(i, components):
                    components.pop(i, None)
                    if verify_level(self.adj[i], components):
                        return True
            return False

        def write_component(node, components):
            for d in self.components[node].dependencies:
                if d in components.keys():
                    return False
            print(node) # TODO: Change to call a component method who returns the block of code
            return True

        verify_level(roots, components)

        # TODO: Write the python script on a tmp file

    def __len__(self):
        return len(self.adj)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))

    def __getitem__(self, v):
        return self.adj[v]
