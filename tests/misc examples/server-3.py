import random

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.core import run
from bacpypes.basetypes import BinaryPV
from bacpypes.object import BinaryInputObject, BinaryOutputObject, Property, register_object_type
from bacpypes.errors import ExecutionError
from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject

from misc import VBIdev, VBOdev

DI_devs = [i for i in range(1, 10)]
DO_devs = [i for i in range(11, 20)]

# some debugging
_debug = 0
_log = ModuleLogger(globals())


@bacpypes_debugging
class DIPresentValue(Property):
    def __init__(self, identifier):
        if _debug:
            DIPresentValue._debug("__init__ %r", identifier)
        Property.__init__(
            self, identifier, BinaryPV, default=BinaryPV("inactive"), optional=False, mutable=False
        )

    def ReadProperty(self, obj, arrayIndex=None):
        if _debug:
            DIPresentValue._debug("ReadProperty %r arrayIndex=%r", obj, arrayIndex)

        # access an array
        if arrayIndex is not None:
            raise ExecutionError(
                errorClass="property", errorCode="propertyIsNotAnArray"
            )

        if _debug:
            DIPresentValue._debug("    - read button: %r", obj._dev.read())

        if obj._dev.read() == 'active':
            return "active"

        else:
            return "inactive"

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
        if _debug:
            DIPresentValue._debug(
                "WriteProperty %r %r arrayIndex=%r priority=%r direct=%r",
                obj,
                value,
                arrayIndex,
                priority,
                direct,
            )

        raise ExecutionError(errorClass="property", errorCode="writeAccessDenied")


@bacpypes_debugging
@register_object_type
class DIBinaryInput(BinaryInputObject):
    properties = [DIPresentValue('presentValue')]

    def __init__(self, dev, **kwargs):
        if _debug:
            DIBinaryInput._debug("__init__ %r %r", dev, kwargs)
        BinaryInputObject.__init__(self, **kwargs)

        # create a button object
        self._dev = dev


@bacpypes_debugging
class DOPresentValue(Property):
    def __init__(self, identifier):
        if _debug:
            DOPresentValue._debug("__init__ %r", identifier)
        Property.__init__(
            self, identifier, BinaryPV, default=BinaryPV("inactive"), optional=False, mutable=True
        )

    def ReadProperty(self, obj, arrayIndex=None):
        if _debug:
            DOPresentValue._debug("ReadProperty %r arrayIndex=%r", obj, arrayIndex)

        # access an array
        if arrayIndex is not None:
            raise ExecutionError(
                errorClass="property", errorCode="propertyIsNotAnArray"
            )

        ###TODO: obj._led is the LED object
        if _debug:
            DOPresentValue._debug("    - read dev: %r", obj._dev.read())

        if obj._dev.read() == "active":
            return "active"
        else:
            return "inactive"

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
        if _debug:
            DOPresentValue._debug(
                "WriteProperty %r %r arrayIndex=%r priority=%r direct=%r",
                obj,
                value,
                arrayIndex,
                priority,
                direct,
            )

        # access an array
        if arrayIndex is not None:
            raise ExecutionError(
                errorClass="property", errorCode="propertyIsNotAnArray"
            )

        ###TODO: obj._button is the Button object
        if _debug:
            DOPresentValue._debug("    - write dev: %r", obj._dev)

        # raise ExecutionError(errorClass="property", errorCode="writeAccessDenied")

        if value == "active":
            obj._dev.write("active")
        elif value == "inactive":
            obj._dev.write("inactive")
        else:
            ### TODO: insert correct value error. Below is a placeholder.
            print("invalid value for led. Use 'active' to turn on or 'inactive' to turn off.")


#
#   RPiBinaryOutput
#


@bacpypes_debugging
@register_object_type
class DOBinaryOutput(BinaryOutputObject):
    properties = [DOPresentValue("presentValue")]

    def __init__(self, dev, **kwargs):
        if _debug:
            DOBinaryOutput._debug("__init__ %r %r", dev, kwargs)
        BinaryOutputObject.__init__(self, **kwargs)

        self._dev = dev

#
#   __main__
#


def main():
    # parse the command line arguments
    args = ConfigArgumentParser(description=__doc__).parse_args()

    if _debug:
        _log.debug("initialization")
    if _debug:
        _log.debug("    - args: %r", args)

    # make a device object
    this_device = LocalDeviceObject(
        objectName=args.ini.objectname,
        objectIdentifier=int(args.ini.objectidentifier),
        maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
        segmentationSupported=args.ini.segmentationsupported,
        vendorIdentifier=int(args.ini.vendoridentifier),
    )

    # make a sample application
    this_application = BIPSimpleApplication(this_device, args.ini.address)

    # make the buttons
    for id in DI_devs:
        dev = VBIdev(id)
        n = random.random()
        print(n)
        bio = DIBinaryInput(
            dev,
            objectIdentifier=(DIBinaryInput.objectType, id),
            objectName=f"{n}test"
            # objectName=dev.file,
        )
        _log.debug("    - bio: %r", bio)
        this_application.add_object(bio)

    # make the LEDs
    for id in DO_devs:
        dev = VBOdev(id)
        n = random.random()
        boo = DOBinaryOutput(
            dev,
            objectIdentifier=(DOBinaryOutput.objectType, id),
            # objectName=dev.file,
            objectName=f"{n}test"
        )

        _log.debug("    - boo: %r", boo)
        this_application.add_object(boo)

    _log.debug("running")

    run()

    _log.debug("fini")


if __name__ == "__main__":
    main()