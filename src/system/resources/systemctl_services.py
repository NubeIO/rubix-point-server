import enum
import subprocess

from flask_restful import Resource, reqparse, abort

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
    STOP = 2
    RESTART = 3


class Services(enum.Enum):
    WIRES = 'nubeio-rubix-wires.service'
    PLAT = 'nubeio-wires-plat.service'
    MOSQUITTO = 'mosquitto.service'


def _validate_and_create_action(action) -> str:
    if action.upper() in ServiceAction.__members__.keys():
        return action.lower()
    else:
        abort(400, message='action should be `start | stop | restart`')


def _validate_and_create_service(action, service) -> str:
    if service.upper() in Services.__members__.keys():
        return f'sudo systemctl {action} {Services[service.upper()].value}'
    else:
        abort(400, message=f'service {service} does not exist in our system`')


def _execute_command(cmd):
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    return True


def _systemctl_status_check(service):
    """
    Return True if systemd service is running
    example: check = systemctl_exists('mosquitto')
    """
    try:
        cmd = f'systemctl is-active {service} >/dev/null 2>&1 && echo TRUE || echo FALSE'
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False

    for line in completed.stdout.decode('utf-8').splitlines():
        if 'TRUE' in line:
            return True
    return False


class SystemctlCommand(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, help='action should be `start | stop | restart`', required=True)
        parser.add_argument('service',
                            type=str,
                            help='service type is required example: (wires, mosquitto)',
                            required=True)
        args = parser.parse_args()
        action = _validate_and_create_action(args['action'])
        service = _validate_and_create_service(action, args['service'])
        call = _execute_command(service)
        if call:
            return {"service": f'{call}, worked!'}
        else:
            return {"service": f'{call}, failed!'}, 404


class SystemctlStatus(Resource):
    @classmethod
    def get(cls, service):
        if service.upper() in Services.__members__.keys():
            check = _systemctl_status_check(Services[service.upper()].value)
            if check:
                return {'status': f'{service} is running'}
            else:
                return {'status': f'{service} is not running'}
        else:
            return {'status': f'{service} does not exist in our system'}
