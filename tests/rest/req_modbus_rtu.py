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
    print('please provide network num, device num and point num '
          '(i.e. "this.py 1 2 3" for 1 network with 2 devices with 3 points each')
    exit(1)


ip = "0.0.0.0"
port = 1515

url = f'http://{ip}:{port}/api'
network_url = f'{url}/modbus/networks'
devices_url = f'{url}/modbus/devices'
fc = "READ_HOLDING_REGISTERS"
data_type = "RAW"
points_url = f'{url}/modbus/points'

for n in range(1, networks+1):
    network_obj = {
        "name": f"network_{n}",
        "type": "RTU",
        "enable": True,
        "timeout": 0.2,
        "rtu_port": f"/dev/ttyUSB{n}",
        "rtu_speed": 9600,
    }

    response_n = requests.post(f'{network_url}', data=network_obj)
    network_uuid_uuid = None
    if 200 <= response_n.status_code < 300:
        r_json = response_n.json()
        network_uuid = r_json['uuid']
        print('added network', r_json.get('name'), network_uuid)
    else:
        print('failed to add network', network_obj.get('name'), response_n.reason)
        continue

    for d in range(1, devices+1):

        devices_obj = {
            "name": f'device_{n}_{d}',
            "enable": True,
            "address": d,
            "network_uuid": network_uuid
        }

        response_d = requests.post(f'{devices_url}', data=devices_obj)
        device_uuid = None
        if 200 <= response_d.status_code < 300:
            r_json = response_d.json()
            device_uuid = r_json['uuid']
            print('    added device', r_json.get('name'), device_uuid)
        else:
            print('    failed to add device', devices_obj.get('name'), response_d.reason)
            continue

        for r in range(1, points+1):
            name = f'point_{n}_{d}_{r}'
            point_obj = {
                "name": f'{name}\\{d}\\{r}',
                "register": r,
                "register_length": 2,
                "function_code": fc,
                "enable": True,
                "data_type": data_type,
                "data_endian": "BEB_LEW",
                "data_round": 2,
                "device_uuid": device_uuid
            }
            response_p = requests.post(f'{points_url}', data=point_obj)
            if 200 <= response_p.status_code < 300:
                r_json = response_p.json()
                print('        added point', r_json.get('name'), r_json.get('uuid'))
            else:
                print('        failed to add point', point_obj.get('name'), response_p.reason)
                continue