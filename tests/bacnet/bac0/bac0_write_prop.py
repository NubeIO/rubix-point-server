import BAC0

from tests.bacnet.bac0.device_test_settings import test_device_url, net_url, test_device

bacnet = BAC0.connect(ip=net_url)

print(test_device_url)
test_device = test_device["network_device_id"]
print(test_device)

address = test_device_url
obj = "analogOutput"
obj_instance = "1"
prop = "presentValue"
value = 99
priority = 8

# bacnet.write('address object object_instance property value - priority')
write = f"{test_device_url} {obj} {obj_instance} {prop} {value} - {priority}"
print(write)
bacnet.write(write)
# write = bacnet.write('192.168.0.202/24:47808 analogOutput 1 presentValue 67 - 10')


prop = "presentValue"

# device = BAC0.device(test_device_url, test_device,bacnet,poll=0, history_size=1)
readObj = f"{test_device_url} {obj} {obj_instance}  {prop}"
read = bacnet.read(readObj)
print(read)

prop = "priorityArray"
readObj = f"{test_device_url} {obj} {obj_instance}  {prop}"
read = bacnet.read(readObj)
print(read.__dict__)
