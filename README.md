# BACnet/IP, Modbus Master and Modbus RTU RESTful APIs

#### How to run

### Installing (for linux)

```
cd bac-rest/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

## License

### Installing (for BBB)

```bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python3-pip virtualenv -y
pip install -U pip setuptools wheel
rm -r venv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 run.py
```

```
sudo journalctl -f -u nubeio-bac-rest.service
sudo systemctl start nubeio-bac-rest.service
sudo systemctl stop nubeio-bac-rest.service
sudo systemctl restart nubeio-bac-rest.service
```

```

### Had to update the BBB from 3.5 to 3.7 but didn't work

```bash
sudo apt update
sudo apt install software-properties-common
## had issue on install and needed to install this
sudo apt-get install dirmngr
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
```



**Initial MQTT client**
publishes on COV
  
topic:
```
rubix/points/{source_driver}/{network_uuid}/{network_name}/{device_uuid}/{device_name}/{point.uuid}/{point.name}/data

[optional] (value only)
rubix/points/{source_driver}/{network_uuid}/{network_name}/{device_uuid}/{device_name}/{point.uuid}/{point.name}/value
rubix/points/3{source_driver}/4{network_uuid}/5{network_name}/6{device_uuid}/7{device_name}/8{point.uuid}/9{point.name}/value
```


example topics:
```
all points:
rubix/points/+/+/+/+/+/data

all modbus rtu points:
rubix/points/modbus_rtu/+/+/+/+/data

by point uuid:
rubix/points/modbus_rtu/+/+/example_point_uuid/+/data

by point name:
rubix/points/modbus_rtu/+/+/+/example_point_name/data

by device name:
rubix/points/modbus_rtu/+/+/+/device 2/+/+/data

by device name:
rubix/points/modbus_rtu/+/+/+/device 2/+/+/data

by network name:
rubix/points/modbus_rtu/+/mod_network_name hey/+/+/+/+/data
```
Other changes:
- `network`, `device`, `point` names can no longer contain forward slash (`/`)
- event services now have a `threaded` flag which dictates whether an event of the subscribing service will be run by the publishing service or added to the event queue or the subscribing service. This will probs be changed in future to be method independent
  

