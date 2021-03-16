from src.resources.utils import map_rest_schema

schedule_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    }
}

schedule_return_attributes = {
    'uuid': {
        'type': str,
    },
    'name': {
        'type': str,
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    }
}

schedule_all_fields = {}
map_rest_schema(schedule_return_attributes, schedule_all_fields)
map_rest_schema(schedule_all_attributes, schedule_all_fields)
