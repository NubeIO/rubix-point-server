import random

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.errors import ExecutionError
from bacpypes.object import AnalogInputObject, BinaryInputObject, MultiStateInputObject
from bacpypes.object import AnalogOutputObject, BinaryOutputObject, MultiStateOutputObject
from bacpypes.object import AnalogValueObject, BinaryValueObject, MultiStateValueObject
from bacpypes.object import Property
from bacpypes.primitivedata import Real

_debug = 1
_log = ModuleLogger(globals())


class RandomValueProperty(Property):

    def __init__(self, identifier):
        if _debug: RandomValueProperty._debug("__init__ %r", identifier)
        Property.__init__(self, identifier, Real, default=0.0, optional=True, mutable=False)

    def ReadProperty(self, obj, arrayIndex=None):
        if _debug: RandomValueProperty._debug("ReadProperty %r arrayIndex=%r", obj, arrayIndex)

        # access an array
        if arrayIndex is not None:
            raise ExecutionError(errorClass='property', errorCode='propertyIsNotAnArray')

        # return a random value
        value = random.random() * 100.0
        if _debug: RandomValueProperty._debug("    - value: %r", value)

        return value

    def WriteProperty(self, obj, value, arrayIndex=None, priority=None, direct=False):
        if _debug: RandomValueProperty._debug("WriteProperty %r %r arrayIndex=%r priority=%r direct=%r", obj, value,
                                              arrayIndex, priority, direct)
        raise ExecutionError(errorClass='property', errorCode='writeAccessDenied')


class RandomInputProperty(RandomValueProperty):
    pass


class RandomOutputProperty(RandomValueProperty):
    pass


bacpypes_debugging(RandomValueProperty)


class RandomAnalogValueObject(AnalogValueObject):
    properties = [
        RandomValueProperty('presentValue'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomAnalogValueObject._debug("__init__ %r", kwargs)
        AnalogValueObject.__init__(self, **kwargs)


class RandomBinaryValueObject(BinaryValueObject):
    properties = [
        RandomValueProperty('presentValue'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomBinaryValueObject._debug("__init__ %r", kwargs)
        BinaryValueObject.__init__(self, **kwargs)


class RandomMultiStateValueObject(MultiStateValueObject):
    properties = [
        RandomValueProperty('presentValue'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomMultiStateValueObject._debug("__init__ %r", kwargs)
        MultiStateValueObject.__init__(self, **kwargs)


class RandomAnalogInputObject(AnalogInputObject):
    properties = [
        RandomInputProperty('presentInput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomAnalogInputObject._debug("__init__ %r", kwargs)
        AnalogInputObject.__init__(self, **kwargs)


class RandomBinaryInputObject(BinaryInputObject):
    properties = [
        RandomInputProperty('presentInput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomBinaryInputObject._debug("__init__ %r", kwargs)
        BinaryInputObject.__init__(self, **kwargs)


class RandomMultiStateInputObject(MultiStateInputObject):
    properties = [
        RandomInputProperty('presentInput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomMultiStateInputObject._debug("__init__ %r", kwargs)
        MultiStateInputObject.__init__(self, **kwargs)


class RandomAnalogOutputObject(AnalogOutputObject):
    properties = [
        RandomOutputProperty('presentOutput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomAnalogOutputObject._debug("__init__ %r", kwargs)
        AnalogOutputObject.__init__(self, **kwargs)


class RandomBinaryOutputObject(BinaryOutputObject):
    properties = [
        RandomOutputProperty('presentOutput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomBinaryOutputObject._debug("__init__ %r", kwargs)
        BinaryOutputObject.__init__(self, **kwargs)


class RandomMultiStateOutputObject(MultiStateOutputObject):
    properties = [
        RandomOutputProperty('presentOutput'),
    ]

    def __init__(self, **kwargs):
        if _debug: RandomMultiStateOutputObject._debug("__init__ %r", kwargs)
        MultiStateOutputObject.__init__(self, **kwargs)
