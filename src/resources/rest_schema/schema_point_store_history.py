from flask_restful import fields

point_store_history_fields = {
    'id': fields.Integer,
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_original': fields.Float,
    'value_raw': fields.String,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts_value': fields.String,
    'ts_fault': fields.String
}

paginated_point_store_history_fields = {
    "page": fields.Integer,
    "per_page": fields.Integer,
    "pages": fields.Integer,
    "total": fields.Integer,
    "has_prev": fields.Boolean,
    "prev_num": fields.Integer,
    "has_next": fields.Boolean,
    "next_num": fields.Integer,
    "items": fields.Nested(point_store_history_fields)
}
