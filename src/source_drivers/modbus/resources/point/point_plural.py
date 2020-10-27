import uuid
from flask_restful import marshal_with
from src.source_drivers.modbus.models.point import ModbusPointModel
from src.source_drivers.modbus.resources.mod_fields import point_fields
from src.source_drivers.modbus.resources.point.point_base import ModbusPointBase
from src.utils.model_utils import ModelUtils


class ModbusPointPlural(ModbusPointBase):
    def get(self):
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
            serialized_output.append({**ModelUtils.row2dict(row), "point_store": self.create_point_store(row.value)})
        return serialized_output, 200

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = ModbusPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)
