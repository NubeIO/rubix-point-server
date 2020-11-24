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

Install the service

```
git clone --depth 1 https://github.com/NubeDev/bac-rest
cd bac-rest/
sudo apt-get install python3-venv -y && python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt 

nano systemd/nubeio-bac-rest.service

python run.py
# install the service
sudo cp systemd/nubeio-bac-rest.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable nubeio-bac-rest.service && sudo journalctl -f -u nubeio-bac-rest.service
# check its running
sudo systemctl restart nubeio-bac-rest.service
sudo journalctl -f -u nubeio-bac-rest.service
```

```
[Unit]
Description=Flask Application for Nube Rest API
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/bac-rest
ExecStart=/home/pi/bac-rest/venv/bin/python run.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=bac-rest

[Install]
WantedBy=multi-user.target
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
  
topic structure:
```
rubix/points/{source_driver}/{network_uuid}/{network_name}/{device_uuid}/{device_name}/{point.uuid}/{point.name}/data

[optional] (value only)
rubix/points/{source_driver}/{network_uuid}/{network_name}/{device_uuid}/{device_name}/{point.uuid}/{point.name}/value
```


example topics:
```
all points:
rubix/points/+/+/+/+/+/+/+/data

all modbus rtu points:
rubix/points/modbus_rtu/+/+/+/+/+/+/data

by point uuid:
rubix/points/+/+/+/+/+/example_point_uuid/+/data

by point name:
rubix/points/+/+/+/+/+/+/example_point_name/data

by device uuid:
rubix/points/+/+/+/example_device_uuid/+/+/+/data

by device name:
rubix/points/+/+/+/+/example_device_name/+/+/data

by network uuid:
rubix/points/+/example_network_uuid/+/+/+/+/+/data

by network name:
rubix/points/+/+/example_network_name/+/+/+/+/data
```
