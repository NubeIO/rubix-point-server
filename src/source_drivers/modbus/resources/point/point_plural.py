import uuid
from flask_restful import marshal_with
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.mod_fields import point_fields
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils


class ModbusPointPlural(ModbusPointBase):
    @classmethod
    @marshal_with(point_fields)
    def get(cls):
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
        return points

    @classmethod
    @marshal_with(point_fields)
    def post(cls):
        _uuid = str(uuid.uuid4())
        data = ModbusPointPlural.parser.parse_args()
        return cls.add_point(data, _uuid)
