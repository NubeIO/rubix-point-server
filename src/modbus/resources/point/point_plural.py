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
        partition_table = db.session.query(ModbusPointStoreModel, func.rank()
                                           .over(order_by=ModbusPointStoreModel.ts.desc(),
                                                 partition_by=ModbusPointStoreModel.point_uuid)
                                           .label('rank')).subquery()

        filtered_partition_table = db.session.query(partition_table).filter(partition_table.c.rank == 1).subquery()
        joined_table = db.session \
            .query(ModbusPointModel, filtered_partition_table) \
            .select_from(ModbusPointModel) \
            .join(filtered_partition_table, ModbusPointModel.uuid == filtered_partition_table.c.point_uuid,
                  isouter=True).all()
        db.session.close()
        serialized_output = []
        for row in joined_table:
            serialized_output.append({**ModelUtils.row2dict(row[0]), "point_store": self.create_point_store(row)})
        return serialized_output, 200

    @marshal_with(point_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = ModbusPointPlural.parser.parse_args()
        return self.add_point(data, _uuid)
