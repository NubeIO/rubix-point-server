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
ExecStart=/home/pi/bac-rest/venv/bin/gunicorn -b 0.0.0.0:1515 --log-level=DEBUG -w 1 run:app
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

Using the API

```
1- in rest api /network we need to add your PC ip the ip that will talk to the BACnet device
2- once a new network is added copy the network_uuid
3- add a /device and use the network_uuid
4- once added copy the network_uuid and bacnet_network_uuid
5- /devices/points/obj and paste in your UUIDs   http://127.0.0.1:5000/api/bacnet/device/points/obj/d0554857-47df-4100-bf6c-43deafb9aa88,5430510a-f0d9-49be-abcc-ddcbf35eb21b
```
