




import BAC0

from device_test_settings import  test_device_url, net_url, test_device



bacnet = BAC0.lite(ip=net_url)
print(test_device_url)
test_device = test_device["network_device_id"]
print(test_device)

address = test_device_url
obj = "analogInput"
obj_instance = "1"
prop = "presentValue"


device = BAC0.device(test_device_url, test_device,bacnet,poll=0, history_size=1)
print(device.points)



find_overrides = device.find_overrides()
print(find_overrides)
# https://bac0.readthedocs.io/en/latest/_modules/BAC0/core/devices/Points.html?highlight=Is_overridden
is_overridden= device['AO 2'].__getitem__("presentValue")
print(is_overridden)
# device.release_all_overrides()
# device['point'].is_overridden