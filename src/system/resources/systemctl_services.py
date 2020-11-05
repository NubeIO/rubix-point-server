import enum
import subprocess

from flask_restful import Resource, reqparse

'''
sudo systemctl start nubeio-rubix-wires.service
sudo systemctl stop nubeio-rubix-wires.service
sudo systemctl restart nubeio-rubix-wires.service
sudo systemctl status nubeio-bac-rest.service
'''
'''
sudo systemctl status nubeio-bac-rest.service
sudo systemctl start nubeio-bac-rest.service
sudo systemctl stop nubeio-bac-rest.service
sudo systemctl restart nubeio-bac-rest.service
'''
'''
sudo systemctl start nubeio-wires-plat.service
sudo systemctl stop nubeio-wires-plat.service
sudo systemctl status nubeio-wires-plat.service
sudo systemctl restart nubeio-wires-plat.service
'''


class ServiceAction(enum.Enum):
    START = 1
    start = 2
    STOP = 3
    stop = 4
    RESTART = 5
    restart = 6


class Services(enum.Enum):
    WIRES = 1
    wires = 2
    PLAT = 3
    plat = 4
    MOSQUITTO = 5
    mosquitto = 6


def _action(action):
    if action in ServiceAction.__members__.keys():
        action = action.lower()
        if action == 'start':
            return "start"
        if action == 'stop':
            return "stop"
        if action == 'restart':
            return "restart"
    else:
        return None


def _service(action, service):
    if service in Services.__members__.keys():
        service = service.lower()
        if service == 'wires':
            return f'sudo {action} nubeio-rubix-wires.service'
        if service == 'plat':
            return f'sudo {action} nubeio-wires-plat.service'
        if service == 'mosquitto':
            return f'systemctl {action} mosquitto'
    else:
        return None


def _system_call(cmd):
    """ Start systemd service."""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    return True


def _systemctl_exists(_service):
    """Return True if systemd service is running
        example: check = systemctl_exists('mosquitto')
    """
    try:
        cmd = f'systemctl is-active {_service} >/dev/null 2>&1 && echo TRUE || echo FALSE'
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        return False
    else:
        for line in completed.stdout.decode('utf-8').splitlines():
            print(line, 11111)
            if 'TRUE' in line:
                return True
        return False


class SystemctlCommand(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, help='action is required (start, stop, restart)', required=True)
        parser.add_argument('service', type=str, help='service type is required example: (wires, mosquitto)', required=True)
        args = parser.parse_args()
        act = _action(args['action'])
        if act is None:
            return {"action_required": False}, 404
        ser = _service(args['service'], act)
        if ser is None:
            return {"service_required": False}, 404
        check = _system_call(act)
        if check:
            return {"system_call": True}
        else:
            return {"system_call": False}, 404


class SystemctlExists(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('service', type=str, help='service type is required example: (wires, mosquitto)', required=True)
        args = parser.parse_args()
        ser = args['service']
        ser = ser.lower()
        if ser in Services.__members__.keys():
            ser = ser.lower()
            check = _systemctl_exists(ser)
            if check:
                return {"check_service": check}
            else:
                return {"check_service": check}
        else:
            return {"check_service": f'{ser} not exists'}
