# BACnet/IP, Modbus Master and Modbus RTU RESTful APIs

## Install

```bash
git clone --depth 1 https://github.com/NubeDev/bac-rest && cd bac-rest/
```

#### RPi

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
mkdir /data/bac-rest
cp settings/config.example.ini /data/bac-rest/config.ini

# copy and edit service file
sudo cp systemd/nubeio-bac-rest.service /etc/systemd/system/
sudo nano /etc/systemd/system/nubeio-bac-rest.service

# load service
sudo systemctl daemon-reload && sudo systemctl enable nubeio-bac-rest.service
sudo systemctl start nubeio-bac-rest.service

# check its running
sudo journalctl -f -u nubeio-bac-rest.service
```
Other:
```
sudo systemctl start nubeio-bac-rest.service
sudo systemctl stop nubeio-bac-rest.service
sudo systemctl restart nubeio-bac-rest.service
sudo journalctl -f -u nubeio-bac-rest.service
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
