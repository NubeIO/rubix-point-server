# api.add_resource(Device, f'/{api_ver}/device/<string:name>')
import json

import requests
from app import ip, port, api_ver

ip = f'http://{ip}:{port}/{api_ver}'

networks = requests.get(f'{ip}/networks')

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
# 1: api call to /networks/UUID to get the network details. Like network IP
# 2: api call to /device/UUID to filter out the devices with that network_uuid


# networks_as_json = networks.json()
# print("TYPE OFF:", type(networks_as_json))
# print(networks_as_json)
# print(networks_as_json['networks'])
#
# network_uuid = networks_as_json['networks'][0]['network_uuid']
# print(network_uuid)
#
# all_network_uuid = networks_as_json['networks']
# for f in all_network_uuid:
#     print(f['network_uuid'])


devices = requests.get(f'{ip}/devices')
devices_as_json = devices.json()
print(devices_as_json)

n = {}

all_device_uuid = devices_as_json['devices']
print("get keys")
for key in all_device_uuid:
    print(key)
print("get items")
for item in all_device_uuid:
    print(item.items())
print("get values")
for item in all_device_uuid:
    print(item.values())

# all_device_uuid = devices_as_json['devices']
# for f in all_device_uuid:
#     n[f] = all_device_uuid[f]
# print(n)
