import BAC0

from tests.bacnet.bac0.device_test_settings import test_device_url, net_url, test_device, test_device_id

bacnet = BAC0.lite(ip=net_url)
print(test_device_url)
test_device = test_device["network_device_id"]
print(test_device)

address = test_device_url
obj = "analogInput"
obj_instance = "1"
prop = "presentValue"

device = BAC0.device(test_device_url, test_device, bacnet, poll=0, history_size=0)
properties = device.bacnet_properties

# read the device name
propType = "device"
propToRead = "objectName"
name = f"{propType}", f"{test_device_id}", f"{propToRead}"
# prop = ('device',100,'objectName')
# name = device.read_property(prop)


# this will return the object name
propType = "device"
propToRead = "objectName"
prop = f"{propType}", f"{test_device_id}", f"{propToRead}"
# prop = ('device',100,'objectName')
pointArray = ('analogOutput', 1, 'priorityArray')
# pointArray = device.read_property(pointArray)


print('device props')
print(properties)
print('device name')
# print(name)
print('device points')
print(device.points)
print('pointArray')
print(pointArray)

import time

time.sleep(1)
device.update_bacnet_properties()
print('device points')
print(device.points)

# this will be a BACnet points discover (if dev already exist you need to unregister_device())
import time

time.sleep(12)
bacnet.unregister_device(device)
print('device disconnect to get new points')
device = BAC0.device(test_device_url, test_device, bacnet, poll=0, history_size=0)
prop = ('analogOutput', 1, 'priorityArray')
priorityArray = device.read_property(prop)
# print(priorityArray.__dict__.keys())
print('device points')
print(device.points)
