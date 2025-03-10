
import json

PRETTY_INDENT = 4

class Chart:

    def __init__(self):
        self._spec = { 'source': [], 'representation': []}

    def source(self, name, source):
        self._spec['source'].append({'name': name, 'source': source})
        return self
    
    # def add_representation(self, name, representation):
    #     self.spec['representation'].append({'name': name

    def add_layer(self):
        layer = Layer()
        self._spec['representation'].append(layer)
        return layer

    def to_json(self, pretty=False):
        # handle inner object serialization
        def custom_serialization(obj):
            if isinstance(obj, Layer):
                return obj.__json__()
            raise TypeError(f"Type {type(obj)} not serializable")

        return json.dumps(self._spec, default=custom_serialization, indent=PRETTY_INDENT if pretty else None)
    
    def to_dict(self):
        return json.loads(self.to_json())

class Layer:
    def __init__(self):
        self._state = { 'mark': None, 'mapping': [] }

    def mark(self, mark: str):
        self._state['mark'] = mark
        return self

    def map(self, encoding: str, **kwargs):
        new_mapping = { 'encoding': encoding }
        if 'field' in kwargs:
            new_mapping['field'] = kwargs['field']
        if 'type' in kwargs:
            new_mapping['type'] = kwargs['type']
        if 'value' in kwargs:
            new_mapping['value'] = kwargs['value']
        self._state['mapping'].append(new_mapping)
        return self
    
    def __json__(self):
        # Return a dictionary that can be serialized by json
        return self._state