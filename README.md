# BACnet/IP, Modbus Master and Modbus RTU RESTful APIs

## Install


### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:
```bash
sudo bash script.bash start -u=<pi|debian> -dir=<point-server_dir> -lib_dir=<common-py-libs-dir>
sudo bash script.bash -h
```

##### Note: _change /data/bac-flask/config.ini  as you want and restart -- `sudo bash script.bash restart`_

### RPi

Dependencies:
```bash
sudo apt install -y python3-venv -y
```
Activate venv:
```bash
python3 -m venv venv && source venv/bin/activate
```
Other:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### BBB

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

## Running (linux)

**Manually**  
(make sure `venv` still active. If not, follow above commands for `venv`)
```bash
python3 run.py
```
**System Service**
```bash
mkdir /data/point-server
cp settings/config.example.ini /data/point-server/config.ini

# copy and edit service file
sudo cp systemd/nubeio-point-server.service /etc/systemd/system/
sudo nano /etc/systemd/system/nubeio-point-server.service

# load service
sudo systemctl daemon-reload && sudo systemctl enable nubeio-point-server.service
sudo systemctl start nubeio-point-server.service

# check its running
sudo journalctl -f -u nubeio-point-server.service
```
Other:
```
sudo systemctl start nubeio-point-server.service
sudo systemctl stop nubeio-point-server.service
sudo systemctl restart nubeio-point-server.service
sudo journalctl -f -u nubeio-point-server.service
```

## DOCS

### Config

#### Development
```bash
cp settings/config.example.ini settings/config.ini
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
