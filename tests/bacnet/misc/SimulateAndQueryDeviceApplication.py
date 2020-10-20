import asyncio
import threading

from src.local_device_applications import LocalDeviceApplication, ReadAllObjectPropertiesApp

'''
Class for simulating a BACnet device and then querying it of it's objects.
'''


def run_application(**kwargs) -> str:
    '''
    Simulates the device given the specified arguments and returns the query of it's objects.
    :param kwargs: Specifies all the objects that are going to be defined for the simulated device.
    :return: Result of querying the device for its objects.
    '''

    # Thread for simulating device
    thread = threading.Thread(target=LocalDeviceApplication.run_application, kwargs=kwargs)
    thread.start()

    # Give object identifier of the device object that will be queried.
    ReadAllObjectPropertiesApp.run_application(kwargs["objectIdentifier"])

    asyncio.get_event_loop().run_until_complete(asyncio.wait_for(ReadAllObjectPropertiesApp.query_output, timeout=30))

    LocalDeviceApplication.stop_application()

    thread.join()

    return ReadAllObjectPropertiesApp.query_output.result()
