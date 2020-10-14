import BAC0

from device_test_settings import  test_device_url, net_url, test_device, test_device_id



bacnet = BAC0.lite(ip=net_url)
print(test_device_url)
test_device = test_device["network_device_id"]
print(test_device)

address = test_device_url
obj = "analogInput"
obj_instance = "1"
prop = "presentValue"


device = BAC0.device(test_device_url, test_device,bacnet,poll=0, history_size=1)
properties = device.bacnet_properties
# print(properties)


# read the device name
propType = "device"
propToRead = "objectName"
prop = f"{propType}", f"{test_device_id}", f"{propToRead}"
# prop = ('device',100,'objectName')
prop = device.read_property(prop)
print(prop)



# this will return the object name
propType = "device"
propToRead = "objectName"
prop = f"{propType}", f"{test_device_id}", f"{propToRead}"
# prop = ('device',100,'objectName')
prop = ('analogOutput',1,'priorityArray')
prop = device.read_property(prop)

print(prop)



