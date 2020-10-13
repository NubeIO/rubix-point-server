# api.add_resource(Device, f'/{api_ver}/device/<string:name>')
import json

import requests
from bacnet.routes import api_ver
from run import ip, port

url = f'http://{ip}:{port}/{api_ver}'

# define bacnet network
# bacnet = BAC0.lite(ip=network_ip, deviceId=network_bacnet_id, localObjName= network_bacnet_name)
# read all the device points
# read=bacnet.read("device_ip device_id objectList")

# deviceIp = "192.168.0.202" # example
# deviceId = "202" # example
# dev = BAC0.device(deviceIp, deviceId,bacnet,poll=0, history_size=0)
# print(dev.points) get all points
# print(dev["AI 1"]) get a point
# print(dev["AI 1"].value) get a point value
# print(dev["AI 1"].units) get a point units

# user to call end point /device/UUID
# user to call api call to /device/point/obj/device_UUID, need to also pass in the network _id

# /network/UUID to get the bacnet network details


# /networks
# {
#     "networks": [
#         {
#             "network_uuid": "5430510a-f0d9-49be-abcc-ddcbf35eb21b",
#             "network_ip": "192.168.20.1",
#             "network_mask": 23,
#             "network_port": 47808,
#             "bacnet_network_id": 3,
#             "network_device_id": 3,
#             "network_device_name": " my device is on 5430510a"
#         },
#         {
#             "network_uuid": "12368c56-eff1-4b6a-8a99-04cb926cbc00",
#             "network_ip": "192.111.20.22",
#             "network_mask": 24,
#             "network_port": 22,
#             "bacnet_network_id": 3,
#             "network_device_id": 3,
#             "network_device_name": "my bac name"
#         }
#     ]
# }


# /devices
# {
#     "devices": [
#         {
#             "bac_device_uuid": "d0554857-47df-4100-bf6c-43deafb9aa88",
#             "bac_device_mac": 111,
#             "bac_device_id": 111,
#             "bac_device_ip": "192.168.20.11",
#             "network_uuid": "5430510a-f0d9-49be-abcc-ddcbf35eb21b"
#         },
#         {
#             "bac_device_uuid": "8acac82b-55dd-4a41-907b-6e33d34d71a2",
#             "bac_device_mac": 22,
#             "bac_device_id": 22,
#             "bac_device_ip": "192.168.20.22",
#             "network_uuid": "5430510a-f0d9-49be-abcc-ddcbf35eb21b"
#         },
#         {
#             "bac_device_uuid": "a54fafca-d2b0-4899-93d1-6e94c1d275e6",
#             "bac_device_mac": 33,
#             "bac_device_id": 33,
#             "bac_device_ip": "192.168.20.33",
#             "network_uuid": "12368c56-eff1-4b6a-8a99-04cb926cbc00"
#         },
#         {
#             "bac_device_uuid": "21fbb8e7-0da7-4717-a866-df113f18f9ec",
#             "bac_device_mac": 44,
#             "bac_device_id": 44,
#             "bac_device_ip": "192.168.20.44",
#             "network_uuid": "12368c56-eff1-4b6a-8a99-04cb926cbc00"
#         }
#     ]
# # }
network_uuid = "5430510a-f0d9-49be-abcc-ddcbf35eb21b"
device_uuid = "d0554857-47df-4100-bf6c-43deafb9aa88"
networks = requests.get(f'{url}/network/{network_uuid}')
networks_as_json = networks.json()
print(networks_as_json)
print("TYPE OFF:", type(networks_as_json))
# print(networks_as_json)
response = networks_as_json
network_uuid = response['network_uuid']
network_ip = response['network_ip']
network_mask = response['network_mask']
network_port = response['network_port']
bacnet_network_id = response['bacnet_network_id']
network_device_id = response['network_device_id']
network_device_name = response['network_device_name']

devices = requests.get(f'{url}/device/{device_uuid}')
response_device = devices.json()

print(response_device)

bac_device_uuid = response_device['bac_device_uuid']
bac_device_mac = response_device['bac_device_mac']
bac_device_id = response_device['bac_device_id']
bac_device_ip = response_device['bac_device_ip']
bac_device_port = response_device['bac_device_port']
bac_network_uuid = response_device['network_uuid']

net_url = f'{network_ip}:{network_port}/{bac_device_port}'

bacnet_network = {
    'net_url': net_url,
    'network_device_id': network_device_id,
    'network_device_name': network_device_name
}

dev_url = f'{bac_device_ip}:{bac_device_port}'

bacnet_device = {
    'dev_url': dev_url,
    'bac_device_id': bac_device_id,

}

print(bacnet_network)
print(bacnet_device['dev_url'])
# print(bacnet_device['dev_url'])
# bacnet = BAC0.lite(ip=network_ip, deviceId=network_bacnet_id, localObjName= network_bacnet_name)
# dev = BAC0.device(deviceIp, deviceId,bacnet,poll=0, history_size=0)

# network_uuid = networks_as_json['networks'][0]['network_uuid']
# print(network_uuid)
#
# all_network_uuid = networks_as_json['networks']
# for f in all_network_uuid:
#     print(f['network_uuid'])


# devices = requests.get(f'{ip}/devices')
# devices_as_json = devices.json()
# print(devices_as_json)
#
# n = {}
#
# all_device_uuid = devices_as_json['devices']
# print("get keys")
# for key in all_device_uuid:
#     print(key)
# print("get items")
# for item in all_device_uuid:
#     print(item.items())
# print("get values")
# for item in all_device_uuid:
#     print(item.values())

# all_device_uuid = devices_as_json['devices']
# for f in all_device_uuid:
#     n[f] = all_device_uuid[f]
# print(n)
