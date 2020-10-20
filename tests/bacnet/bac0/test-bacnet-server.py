##The following code connects to a DXR and then command damper position open adn readys flow back
# The following modules need to be enabled via [pip python "module"]

import time

# hvac = BAC0.lite(port=47801)
# temp = create_AV(oid=1, name="temp", pv=12.8, pv_writable=True)
# temp.units = EngineeringUnits.enumerations["degreesCelsius"]
# temp.description = "AVG Temp"
# hvac.this_application.add_object(temp)
# ip = hvac.localIPAddr.addrTuple[0]
# boid = hvac.Boid
# bacnet = BAC0.lite()
# test_device = BAC0.device("{}:47808".format(ip), boid, bacnet, poll=10)
# print(boid)
# params = namedtuple(
#     "devices",
#     ["bacnet", "hvac", "test_device",],
#     )
# params.bacnet = bacnet
# params.hvac = hvac
# params.test_device = test_device
# params.test_device.disconnect()
# params.bacnet.disconnect()
import BAC0
from BAC0.core.devices.create_objects import create_AV
from BAC0.tasks.RecurringTask import RecurringTask
from bacpypes.primitivedata import Real


# hvac = BAC0.lite(port=47808)
# temp = create_AV(oid=1, name="temp", pv=12.8, pv_writable=True)
# temp.units = EngineeringUnits.enumerations["degreesCelsius"]
# temp.description = "AVG Temp"
# hvac.this_application.add_object(temp)


def changeValueOfMyAI():
    obj = bacnet.this_application.get_object_name('MyAI')
    value = obj.ReadProperty('presentValue').value
    value = value + 1 if value < 100 else 0
    obj.presentValue = Real(value)


ip = '192.168.0.100/24:47808'
deviceId = 100
localObjName = "BAC0_Fireplace"

# ip = None,
# port = None,
# mask = None,
# bbmdAddress = None,
# bbmdTTL = 0,
# ping = True,


bacnet = BAC0.lite(ip=ip, deviceId=deviceId, localObjName=localObjName)
# bacnet = BAC0.lite()
# bacnet = BAC0.lite(ip='192.168.0.100/24:47808')
bacnet.this_application.add_object(create_AV(oid=0, name='MyAI', pv=Real(0), pv_writable=True))
bacnet.this_application.add_object(create_AV(oid=2, name='MyAI2', pv=Real(0), pv_writable=True))
# bacnet.this_application.add_object(create_AI(oid=0, name='MyAI', pv=Real(0)))

task = RecurringTask(changeValueOfMyAI, delay=5)
task.start()

while True:
    obj = bacnet.this_application.get_object_name('MyAI')
    print('Running and value is {}'.format(obj.presentValue))
    time.sleep(20)
