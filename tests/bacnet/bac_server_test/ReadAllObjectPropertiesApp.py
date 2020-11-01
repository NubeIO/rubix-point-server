# #!/usr/bin/env python
#
# """
# File from: https://github.com/JoelBender/bacpypes/blob/master/samples/ReadAllObjectPropertiesApp.py
#
# This application is given the device instance number of a device and its
# address read the object list, then for each object, all properties are read and output.
# """
#
# from collections import deque
#
# from bacpypes.debugging import bacpypes_debugging, ModuleLogger
# from bacpypes.consolelogging import ConfigArgumentParser
#
# from bacpypes.core import run, deferred, stop, run_once
# from bacpypes.iocb import IOCB
#
# from bacpypes.primitivedata import ObjectIdentifier, CharacterString, Atomic
# from bacpypes.constructeddata import ArrayOf
#
# from bacpypes.pdu import Address
# from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK
#
# from bacpypes.app import BIPSimpleApplication
# from bacpypes.local.device import LocalDeviceObject
# from bacpypes.object import Object
#
# from bacpypes.object import get_object_class
#
# import asyncio
#
# import json
#
# _debug = 0
# _log = ModuleLogger(globals())
#
# this_device = None
# this_application = None
# query_output = asyncio.Future()
#
# ArrayOfObjectIdentifier = ArrayOf(ObjectIdentifier)
#
# class ObjectPropertyContext:
#
#     def __init__(self, device_id, device_addr):
#         self.device_id = device_id
#         self.device_addr = device_addr
#
#         self.object_list = []
#         self.object_names = []
#
#         self.current_object_id = None
#         self.current_property = None
#
#         self._object_list_queue = None
#         self.propertyid_dict_queue = None
#         self.property_result_dict = None
#
#     def completed(self, had_error=None):
#         if had_error:
#             print("had error: %r" % (had_error,))
#         else:
#             query_output.set_result(json.dumps(self.property_result_dict, indent=4))
#
#         stop()
#
# @bacpypes_debugging
# class ReadAllObjectPropertiesApplication(BIPSimpleApplication):
#
#     def __init__(self, *args):
#         if _debug: ReadAllObjectPropertiesApplication._debug("__init__ %r", args)
#         BIPSimpleApplication.__init__(self, *args)
#
#     def read_object_list(self, device_id, device_addr):
#         if _debug: ReadAllObjectPropertiesApplication._debug("read_object_list %r %r", device_id, device_addr)
#
#         # create a context to hold the results
#         context = ObjectPropertyContext(device_id, device_addr)
#
#         # build a request for the object name
#         request = ReadPropertyRequest(
#             destination=context.device_addr,
#             objectIdentifier=context.device_id,
#             propertyIdentifier='objectList',
#             )
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - request: %r", request)
#
#         # make an IOCB, reference the context
#         iocb = IOCB(request)
#         iocb.context = context
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - iocb: %r", iocb)
#
#         # let us know when its complete
#         iocb.add_callback(self.object_list_results)
#
#         # give it to the application
#         self.request_io(iocb)
#
#     def object_list_results(self, iocb):
#         if _debug: ReadAllObjectPropertiesApplication._debug("object_list_results %r", iocb)
#
#         # extract the context
#         context = iocb.context
#
#         # do something for error/reject/abort
#         if iocb.ioError:
#             context.completed(iocb.ioError)
#             return
#
#         # do something for success
#         apdu = iocb.ioResponse
#
#         # should be an ack
#         if not isinstance(apdu, ReadPropertyACK):
#             if _debug: ReadAllObjectPropertiesApplication._debug("    - not an ack")
#             context.completed(RuntimeError("read property ack expected"))
#             return
#
#         # pull out the content
#         object_list = apdu.propertyValue.cast_out(ArrayOfObjectIdentifier)
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - object_list: %r", object_list)
#
#         # store it in the context
#         context.object_list = object_list
#
#         #Get the object classes for each object in the object list and get all possible properties that can be queried for each device.
#         object_classes = [(get_object_class(obj[0]),obj[1]) for obj in object_list]
#         context.properties_dict_queue = {(object_class[0].objectType,object_class[1]):deque([(prop.identifier,prop.datatype) for prop in Object.properties+object_class[0].properties]) for object_class in object_classes}
#         context.property_result_dict = dict()
#
#         # make a queue of the identifiers to read, start reading them
#         context._object_list_queue = deque(object_list)
#         deferred(self.read_next_object_properties, context)
#
#     def read_next_object_properties(self, context):
#         if _debug: ReadAllObjectPropertiesApplication._debug("read_next_object %r", context)
#
#         # if there's nothing more to do, we're done
#
#         if all([len(context.properties_dict_queue[element]) == 0 for element in context.properties_dict_queue]):
#             if _debug: ReadAllObjectPropertiesApplication._debug("    - all done")
#             context.completed()
#             return
#
#         # pop off the next object identifier
#         if context.current_object_id is None or len(context.properties_dict_queue[context.current_object_id]) == 0:
#             context.current_object_id = context._object_list_queue.popleft()
#             context.property_result_dict.update({context.current_object_id[0]+str(context.current_object_id[1]):dict()})
#
#         context.current_property = context.properties_dict_queue[context.current_object_id].popleft()
#
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - object_id: %r", context.current_object_id)
#
#         # build a request for the object name
#         request = ReadPropertyRequest(
#             destination=context.device_addr,
#             objectIdentifier=context.current_object_id,
#             propertyIdentifier=context.current_property[0],
#             )
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - request: %r", request)
#
#         # make an IOCB, reference the context
#         iocb = IOCB(request)
#         iocb.context = context
#         if _debug: ReadAllObjectPropertiesApplication._debug("    - iocb: %r", iocb)
#
#         # let us know when its complete
#         iocb.add_callback(self.object_properties_results)
#
#         # give it to the application
#         self.request_io(iocb)
#
#     def object_properties_results(self, iocb):
#         if _debug: ReadAllObjectPropertiesApplication._debug("object_name_results %r", iocb)
#
#         # extract the context
#         context = iocb.context
#
#         #If property is not defined, skip it
#         if iocb.ioError and iocb.ioError.errorCode == 'unknownProperty':
#             deferred(self.read_next_object_properties, context)
#             return
#         elif iocb.ioError and iocb.ioError.errorCode == 'operationalProblem':
#             deferred(self.read_next_object_properties, context)
#             return
#         elif iocb.ioError:  # do something for error/reject/abort
#             context.completed(iocb.ioError)
#             return
#
#         # do something for success
#         apdu = iocb.ioResponse
#
#         # should be an ack
#         if not isinstance(apdu, ReadPropertyACK):
#             if _debug: ReadAllObjectPropertiesApplication._debug("    - not an ack")
#             context.completed(RuntimeError("read property ack expected"))
#             return
#
#         # pull out the name
#         property_reply = apdu.propertyValue.cast_out(context.current_property[1])
#
#         # store it in the context
#         context.property_result_dict[context.current_object_id[0]+str(context.current_object_id[1])][context.current_property[0]] = property_reply
#
#         # read the next one
#         deferred(self.read_next_object_properties, context)
#
# def run_application(objectidentifier: int):
#     global this_device
#     global this_application
#
#     # parse the command line arguments
#     parser = ConfigArgumentParser(description=__doc__)
#
#     # add an argument for interval
#     parser.add_argument('device_id', type=int,
#           help='device identifier',
#           )
#
#     # add an argument for interval
#     parser.add_argument('device_addr', type=str,
#           help='device address',
#           )
#
#     # make a device object
#     this_device = LocalDeviceObject(
#         objectName="objectpropertyreader",
#         objectIdentifier=599,
#         maxApduLengthAccepted=1024,
#         segmentationSupported="segmentedBoth",
#         vendorIdentifier=15,
#     )
#
#     # import netifaces
#     # from ipaddress import IPv4Network
#     #
#     # wifi_ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]
#     # #Addres of this device which will perform the querying.
#     # address = wifi_ip['addr'] + "/" + str(IPv4Network("0.0.0.0/" + wifi_ip['netmask']).prefixlen) + ":47809"
#     address = "0.0.0.0:47807"
#
#     # make a simple application
#     this_application = ReadAllObjectPropertiesApplication(this_device, address)
#
#     # build a device object identifier
#     device_id = ('device', objectidentifier)
#
#     # Address of device being queried.
#     device_addr = "192.168.0.202:47808"
#
#     # kick off the process after the core is up and running
#     deferred(this_application.read_object_list, device_id, device_addr)
#
#     _log.debug("running")
#
#     run()
#
#     _log.debug("fini")