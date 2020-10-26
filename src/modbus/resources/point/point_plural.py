import uuid
from flask_restful import marshal_with
from sqlalchemy import func

from src.modbus.models.point import ModbusPointModel
from src.modbus.resources.mod_fields import point_fields
from src.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils


class ModbusPointPlural(ModbusPointBase):
    def get(self):
        from src import db, ModbusPointStoreModel
        # partition_table = db.session.query(ModbusPointStoreModel, func.rank()
        #                                    .over(order_by=ModbusPointStoreModel.ts.desc(),
        #                                          partition_by=ModbusPointStoreModel.point_uuid)
        #                                    .label('rank')).subquery()

        # filtered_partition_table = db.session.query(partition_table).filter(partition_table.c.rank == 1).subquery()
        # joined_table = db.session \
        #     .query(ModbusPointModel, filtered_partition_table) \
        #     .select_from(ModbusPointModel) \
        #     .join(filtered_partition_table, ModbusPointModel.uuid == filtered_partition_table.c.point_uuid,
        #           isouter=True).all()
        points = ModbusPointModel.query.all()
        serialized_output = []
        for row in points:
            # serialized_output.append({**ModelUtils.row2dict(row)})
            serialized_output.append({**ModelUtils.row2dict(row), "point_store": self.create_point_store(row.value)})
        print(len(serialized_output))
        return serialized_output, 200

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = ModbusPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)


# could be a more efficient way to query this but should be good
class ModbusPointPluralPointStore(ModbusPointBase):
    def get(self, device_uuid):
        from src import db, ModbusPointStoreModel

        device_points = db.session.query(ModbusPointModel) \
            .filter(ModbusPointModel.device_uuid == device_uuid) \
            .subquery()

        partition_table = db.session.query(ModbusPointStoreModel, func.rank()
                                           .over(order_by=ModbusPointStoreModel.ts.desc(),
                                                 partition_by=ModbusPointStoreModel.point_uuid)
                                           .label('rank')) \
            .subquery()
        filtered_partition_table = db.session.query(partition_table).filter(partition_table.c.rank == 1).subquery()

        final = db.session.query(device_points.c.uuid, device_points.c.name, device_points.c.reg,
                                 filtered_partition_table.c.value, filtered_partition_table.c.fault) \
            .select_from(device_points) \
            .join(filtered_partition_table, filtered_partition_table.c.point_uuid == device_points.c.uuid) \
            .all()

        serialized_output = []
        for row in final:
            serialized_output.append({'uuid': row.uuid, 'name': row.name, 'reg': row.reg, 'fault': row.fault,
                                      'value': row.value})
        return serialized_output
