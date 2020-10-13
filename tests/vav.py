
from uuid import uuid4 as gen_uuid

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run

from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject

from bacpypes.constructeddata import ArrayOf
from bacpypes.primitivedata import CharacterString
from bacpypes.basetypes import NameValue
# from bacpypes.service.semantic import SemanticQueryServices

from random_objects import *

_debug = 1
_log = ModuleLogger(globals())

def get_obj_class(obj_type):
    ''.join(obj_type.split(' '))

# VAV tags

znt = [
    ('brick:hasTag', 'bt:Zone'),
    ('brick:hasTag', 'bt:Temperature'),
    ('brick:hasTag', 'bt:Sensor'),
]
zntsp = [
    ('brick:hasTag', 'bt:Zone'),
    ('brick:hasTag', 'bt:Temperature'),
    ('brick:hasTag', 'bt:Setpoint'),
]
dafsp = [
    ('brick:hasTag', 'bt:Discharge'),
    ('brick:hasTag', 'bt:Air'),
    ('brick:hasTag', 'bt:Flow'),
    ('brick:hasTag', 'bt:Setpoint'),
]

daf = [
    ('brick:hasTag', 'bt:Discharge'),
    ('brick:hasTag', 'bt:Air'),
    ('brick:hasTag', 'bt:Flow'),
    ('brick:hasTag', 'bt:Sensor'),
]

vav_point_templates = [zntsp, znt, dafsp, daf]

point_type_rules = {
    ('brick:hasTag', 'bt:Sensor'): 'Input',
    ('brick:hasTag', 'bt:Setpoint'): 'Value',
}
value_type_rules = {
    ('brick:hasTag', 'bt:Flow'): 'Analog',
    ('brick:hasTag', 'bt:Temperature'): 'Analog',
}

class VavDevice(BIPSimpleApplication):
    def __init__(self, *args, vav_nums=1, **kwargs):
        super(VavDevice, self).__init__(*args, **kwargs)
        for _ in range(0, vav_nums):
            vav_id = ':vav-{0}'.format(gen_uuid())
            zone_id = ':zone-{0}'.format(gen_uuid())
            self._register_vav_objs(vav_id, zone_id)

        # self.add_capability(SemanticQueryServices)

    def _register_vav_objs(self, vav_id, zone_id):
        for idx, obj_template in enumerate(vav_point_templates):
            idx += 1
            obj_point_type = None
            for point_type_rule, point_type in point_type_rules.items():
                if point_type_rule in obj_template :
                    obj_point_type = point_type
            assert obj_point_type

            obj_value_type = None
            for value_type_rule, value_type in value_type_rules.items():
                if value_type_rule in obj_template :
                    obj_value_type = value_type
            assert obj_value_type
            obj_typestr = obj_value_type + obj_point_type
            obj_cls = eval('Random{0}Object'.format(obj_typestr))
            name_values = [NameValue(name=name_template, value=CharacterString(value_template))
                           for (name_template, value_template) in obj_template]
            name_values.append(NameValue(name='brick:isPointOf', value=CharacterString(vav_id)))
            name_values.append(NameValue(name='brick:isPointOf', value=CharacterString(zone_id)))
            tags = ArrayOf(NameValue)(name_values)
            obj = obj_cls(
                objectIdentifier=idx + 10,
                objectName='Random{0}-{1}'.format(obj_cls.__name__, idx),
                tags=tags,
            )
            self.add_object(obj)

def main():
    args = ConfigArgumentParser(description=__doc__).parse_args()

    if _debug: _log.debug("initialization")
    if _debug: _log.debug("    - args: %r", args)

    this_device = LocalDeviceObject(
        objectName=args.ini.objectname,
        objectIdentifier=('device', int(args.ini.objectidentifier)),
        maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
        segmentationSupported=args.ini.segmentationsupported,
        vendorIdentifier=int(args.ini.vendoridentifier),
    )

    this_application = VavDevice(this_device, args.ini.address)
    run()

if __name__ == '__main__':
    main()