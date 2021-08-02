from flask import Blueprint
from flask_restful import Api

from src.resources.device.device_plural import DevicePlural
from src.resources.device.device_singular import DeviceSingularByUUID, DeviceSingularByName
from src.resources.network.network_plural import NetworkPlural
from src.resources.network.network_singular import NetworkSingularByUUID, NetworkSingularByName
from src.resources.point.point_plural import PointPlural
from src.resources.point.point_singular import PointSingularByUUID, PointSingularByName, PointNameByUUID
from src.resources.point.point_value_writer import PointUUIDValueWriter, PointNameValueWriter
from src.resources.point.point_store_history import PointStoryHistoryPlural, PointStoreHistoryByPointUUID
from src.resources.schedule.schedule_plural import SchedulePlural
from src.resources.schedule.schedule_singular import ScheduleByUUID, ScheduleByName
from src.system.resources.memory import GetSystemMem
from src.system.resources.ping import Ping

bp_generic = Blueprint('generic', __name__, url_prefix='/api/generic')
api_generic = Api(bp_generic)
api_generic.add_resource(NetworkPlural, '/networks')
api_generic.add_resource(NetworkSingularByUUID, '/networks/uuid/<string:uuid>')
api_generic.add_resource(NetworkSingularByName, '/networks/name/<string:name>')
api_generic.add_resource(DevicePlural, '/devices')
api_generic.add_resource(DeviceSingularByUUID, '/devices/uuid/<string:uuid>')
api_generic.add_resource(DeviceSingularByName, '/devices/name/<string:network_name>/<string:device_name>')
api_generic.add_resource(PointPlural, '/points')
api_generic.add_resource(PointSingularByUUID, '/points/uuid/<string:uuid>')
api_generic.add_resource(PointSingularByName,
                         '/points/name/<string:network_name>/<string:device_name>/<string:point_name>')
api_generic.add_resource(PointUUIDValueWriter, '/points_value/uuid/<string:uuid>')
api_generic.add_resource(PointNameValueWriter,
                         '/points_value/name/<string:network_name>/<string:device_name>/<string:point_name>')
api_generic.add_resource(PointNameByUUID, '/points/get_name/uuid/<string:uuid>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(GetSystemMem, '/memory')
api_system.add_resource(Ping, '/ping')

bp_schedule = Blueprint('schedules', __name__, url_prefix='/api/schedules')
api_schedule = Api(bp_schedule)
api_schedule.add_resource(SchedulePlural, '')
api_schedule.add_resource(ScheduleByUUID, '/uuid/<string:uuid>')
api_schedule.add_resource(ScheduleByName, '/name/<string:name>')

bp_point_store_history = Blueprint('point_store_histories', __name__, url_prefix='/api/point_store_histories')
api_point_store_history = Api(bp_point_store_history)
api_point_store_history.add_resource(PointStoryHistoryPlural, '')
api_point_store_history.add_resource(PointStoreHistoryByPointUUID, '/point_uuid/<string:point_uuid>')
