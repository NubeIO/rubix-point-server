# from flask_restful import Resource, reqparse
# from models.device import DeviceModel
#
#
# class Device(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('device_uuid',
#                         type=str,
#                         required=True,
#                         help='Must pass in the BACnet device uuid'
#                         )
#
#     # mac, bac_device_id , ip, mask, port, network_id
#     # @jwt_required()
#     def get(self, name):
#         uuid = name
#         device = DeviceModel.find_by_uuid(uuid)
#         if device:
#             return device.get_device()
#         return {'message': 'device not found.'}, 404
