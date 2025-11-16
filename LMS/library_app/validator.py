from marshmallow import ValidationError

class SchemaValidator:
    def __init__(self, schemas_module_name=None):
        self.schemas_module_name = schemas_module_name
        self.schemas = {}
        if schemas_module_name:
            self._load_schemas()
    
    def _load_schemas(self):
        try:
            import importlib
            module = importlib.import_module(self.schemas_module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr_name.endswith('Schema'):
                    self.schemas[attr_name] = attr
        except ImportError:
            pass
    
    def validate(self, schema_class, data, partial=False, many=False):
        try:
            schema = schema_class(many=many)
            return schema.load(data, partial=partial)
        except ValidationError as e:
            raise ValidationError(e.messages)
    
    def dump(self, schema_class, obj, many=False):
        schema = schema_class(many=many)
        return schema.dump(obj)