import BAC0
from BAC0.core.io.Write import WriteProperty

from device_test_settings import  test_device_url, net_url, test_device


bacnet1 = BAC0.connect(ip=net_url)
print(test_device_url)
test_device = test_device["network_device_id"]
print(test_device)

address = test_device_url
obj = "analogInput"
obj_instance = "1"
prop = "presentValue"


device = BAC0.device(test_device_url, test_device,bacnet1,poll=0, history_size=1)
# readObj  = f"{test_device_url} {obj} {obj_instance} {prop}"
prop = ('analogOutput',1,'presentValue')
write = bacnet1.write_property(prop,value=98,priority=16)
print(write)

