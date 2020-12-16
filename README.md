# Rubix Point Server

## Install
___

### Production

1. Clone [common-pi-libs](https://github.com/NubeIO/common-py-libs)
   ```
   git clone https://github.com/NubeIO/common-py-libs.git
   ```
2. Install common libs in that directory (follow instructions on [here](https://github.com/NubeIO/common-py-libs#how-to-create))
3. Run install script
   ```
   sudo bash script.bash start --service-name=<service_name> -u=<pi|debian> --dir=<working_dir> --lib-dir=<common-py-libs-dir> --data-dir=<data_dir> -p=<port>
   ```
   i.e.
   ```
   sudo bash script.bash start --service-name=nubeio-point-server.service -u=pi --dir=/home/pi/rubix-point-server --lib-dir=/home/pi/common-py-libs --data-dir=/data/point-server -p=1515
   ```
4. _change /data/point-server/config.ini  as you want and restart -- `sudo bash script.bash restart`_

### Development

#### RPi
Dependencies:
```bash
sudo apt install -y python3-venv
```
Activate venv:
```bash
python3 -m venv venv && source venv/bin/activate
```
Other:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

#### BBB

Dependencies:  
(Had to update the BBB from 3.5 to 3.7 but didn't work)
```bash
sudo apt update
sudo apt install -y software-properties-common

## had issue on install and needed to install this:
sudo apt install -y dirmngr

# Python
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.7
sudo apt install -y build-essential python-dev python-setuptools python-pip python-smbus python3-pip virtualenv -y
pip install -U pip setuptools wheel

rm -r venv
```
Activate venv:
```bash
virtualenv -p python3 venv && source venv/bin/activate
```
Other:
```bash
pip3 install -r requirements.txt
```

#### Running (linux)

(make sure `venv` still active. If not, follow above commands for `venv`)
```bash
python run.py
```

## DOCS
___
### Config

#### Development
```bash
cp settings/config.example.ini settings/config.ini
cp logging/logging.example.conf logging/logging.conf
```

### MQTT client
  
#### Topic structure:
```
rubix/points/{event}/...
```
```
COV:
  rubix/points/cov/all/{point_uuid}/{point_name}/{device_uuid}/{device_name}/{network_uuid}/{network_name}/{source_driver}/

  [optional] (value only)
  rubix/points/cov/value/{point_uuid}/{point_name}/{device_uuid}/{device_name}/{network_uuid}/{network_name}/{source_driver}/

UPDATE:
  rubix/points/update/{model}/{model.uuid}
```


#### Example topics:

**COV:**
```
all points:
  rubix/points/cov/all/#

all modbus rtu points:
  rubix/points/cov/all/+/+/+/+/+/+/modbus_rtu

by point uuid:
  rubix/points/cov/all/example_uuid/#

by point name:
  rubix/points/cov/all/+/example_name/#
```
**UPDATE:**
```
network:
  rubix/points/update/network/example_network_uuid

device:
  rubix/points/update/device/example_device_uuid

point:
  rubix/points/update/point/example_point_uuid
```

### Generic Point MQTT client

All generic point values are updated over MQTT.  
These COVs are then broadcast again over the normal MQTT clients as above
#### Topic structure:
```
rubix/points/generic/cov/<point_name>/<device_name>/<network_name>
```
