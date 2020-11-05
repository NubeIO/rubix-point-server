import sys
import requests

networks = None
devices = None
points = None

if len(sys.argv) == 4:
    networks = int(sys.argv[1])
    devices = int(sys.argv[2])
    points = int(sys.argv[3])
    if networks < 1 or devices < 1 or points < 1:
        print('invalid numbers')
        exit(1)
else:
    print('please provide network num, device num and point num ' \
          '(i.e. "this.py 1 2 3" for 1 network with 2 devices with 3 points each')
    exit(1)


ip = "0.0.0.0"
port = 1515

url = f'http://{ip}:{port}/api'
network_url = f'{url}/modbus/networks'
devices_url = f'{url}/modbus/devices'
reg_type = "READ_HOLDING_REGISTERS"
data_type = "RAW"
points_url = f'{url}/modbus/points'

for n in range(1, networks+1):
    network_obj = {
        "name": f"network_{n}",
        "type": "RTU",
        "enable": True,
        "timeout": 0.2,
        "device_timeout_global": 1000,
        "point_timeout_global": 2000,
        "rtu_port": "/dev/ttyUSB2",
        "rtu_speed": 9600,
        "rtu_stop_bits": 1,
        "rtu_parity": "N",
        "rtu_byte_size": 8
    }

    response_n = requests.post(f'{network_url}', data=network_obj)
    r_json = response_n.json()
    network_uuid = r_json['uuid']
    print('added network', r_json.get('name'), network_uuid)

    for d in range(1, devices+1):

        devices_obj = {
            "name": f'device_{d}',
            "enable": True,
            "type": "RTU",
            "address": d,
            "ping_point_type": "mod_ping_point_type",
            "ping_point_address": 1,
            "zero_mode": False,
            "timeout": 1,
            "timeout_global": False,
            "network_uuid": network_uuid
        }

        response_d = requests.post(f'{devices_url}', data=devices_obj)
        r_json = response_d.json()
        device_uuid = r_json['uuid']
        print('    added device', r_json.get('name'), device_uuid)

        for r in range(1, points+1):
            name = f'point_{r}'
            point_obj = {
                "name": f'{name}/{d}/{r}',
                "reg": r,
                "reg_length": 2,
                "type": reg_type,
                "enable": True,
                "data_type": data_type,
                "data_endian": "BEB_BEW",
                "data_round": 22,
                "data_offset": 2,
                "timeout": 1,
                "timeout_global": True,
                "device_uuid": device_uuid
            }
            response_p = requests.post(f'{points_url}', data=point_obj)
            r_json = response_p.json()
            print('        added point', r_json.get('name'), r_json.get('uuid'))
