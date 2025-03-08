import json

class Chart:

    def __init__(self):
        self._spec = { 'source': [], 'representation': []}

    def source(self, name, source):
        self._spec['source'].append({'name': name, 'source': source})
        return self
    
    # def add_representation(self, name, representation):
    #     self.spec['representation'].append({'name': name

    def to_json(self):
        return json.dumps(self._spec)
