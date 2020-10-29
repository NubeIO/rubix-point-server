#!/usr/bin/env python

"""
Modified version of https://github.com/JoelBender/bacpypes/blob/master/samples/Tutorial/SampleConsoleCmd.py
under MIT license.

Base application for simulating a bacnet device on the local network.
To use the ini arguments of the starting script must be passed and all objects
that are going to be associated with the spoofed device must be passed.
"""

from bacpypes.debugging import bacpypes_debugging, ModuleLogger

from bacpypes.core import run, enable_sleeping, stop

from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject

from bacpypes.object import Object
from typing import List

_debug = 0
_log = ModuleLogger(globals())

this_application = None

@bacpypes_debugging
class DebugApplication(BIPSimpleApplication):
    def __init__(self, device, address):
        if _debug: DebugApplication._debug("__init__ %r %r", device, address)
        BIPSimpleApplication.__init__(self, device, address)

    def request(self, apdu):
        if _debug: DebugApplication._debug("request %r", apdu)
        BIPSimpleApplication.request(self, apdu)

    def indication(self, apdu):
        if _debug: DebugApplication._debug("indication %r", apdu)
        BIPSimpleApplication.indication(self, apdu)

    def response(self, apdu):
        if _debug: DebugApplication._debug("response %r", apdu)
        BIPSimpleApplication.response(self, apdu)

    def confirmation(self, apdu):
        if _debug: DebugApplication._debug("confirmation %r", apdu)
        BIPSimpleApplication.confirmation(self, apdu)

def stop_application():
    stop()

def run_application(**kwargs):
    '''
    Running the base application for spoofing bacnet test_devices on the local network.
    :param vendoridentifier:
    :param segmentationsupported:
    :param maxapdulength:
    :param objectidentifier:
    :param objectname:
    :param ini: Ini parameters
    :param objects: Objects to be attached to the device
    :return:
    '''

    # import netifaces
    # from ipaddress import IPv4Network

    # wifi_ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]
    address = "0.0.0.0:47808"

    this_device = LocalDeviceObject(**kwargs)

    this_application = DebugApplication(this_device, address)

    if "objects" in kwargs.keys():
        for object in kwargs["objects"]:
            this_application.add_object(object)

    enable_sleeping()

    run()