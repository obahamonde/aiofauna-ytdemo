import shelve

import jinja2
from pydantic import BaseModel, create_model

jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        autoescape=jinja2.select_autoescape(['py'])
    )

class Fmt(object):
    def snake_case(self, value):
        for i in [' ', '-', '.']:
            value = value.replace(i, '_')
        return value.lower()
    
    def pascal_case(self, value):
        for i in [' ', '-', '.', '_']:
            value = value.replace(i, '#bizarre#')
        value = ''.join([i.capitalize() for i in value.split('#bizarre#')])
        return value
    
    def field_info(self, value):
        if value is None:
            return 'None'
        if isinstance(value, str):
            return f"'{value}'"
        return value





# Recursive function to create models
def create_dynamic_model(name, **field_definitions):
    DynamicModel = create_model(name, **field_definitions)
    fields = {}
    for field_name, field in DynamicModel.schema()['properties'].items():
        if field.get('type') == 'object':
            field_type = field.get('title')
            if field_type:
                sub_model = create_dynamic_model(field_type, **field.get('properties', {}))
                field_type = sub_model.__name__
            else:
                field_type = 'dict'
        elif field.get('type') == 'array':
            items = field.get('items', {})
            if items.get('type') == 'object':
                field_type = items.get('title')
                if field_type:
                    sub_model = create_dynamic_model(field_type, **items.get('properties', {}))
                    field_type = f"List[{sub_model.__name__}]"
                else:
                    field_type = 'List[dict]'
            else:
                field_type = f"List[{items.get('type')}]"
        else:
            field_type = field.get('type')
            if field_type == 'integer':
                field_type = 'int'
        default = field.get('default')
        default_str = f" = {default}" if default is not None else ""
        fields[field_name] = {'title': field_type, 'default': default_str}
    template = jinja_env.get_template('model.py.j2')
    # Render the template with the class name and fields
    source_code = template.render(class_name=DynamicModel.__name__, fields=fields)
    print(source_code)
    return DynamicModel


from requests import Session


class Docker(Session):
    def get_containers(self):
        return self.get('http://localhost:9898/containers/json').json()
    
schemas = {}

containers = Docker().get_containers()

for container in containers:
    model = create_model(container["Image"], **container)
    field_definitions = model.schema()['properties']
    name = model.schema()['title'].capitalize()
    create_dynamic_model(name, **field_definitions)