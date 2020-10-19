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

#### Create DB

```bash
$ python
>> from bacnet import db
>> db.create_all()
>> exit()
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
5- /devices/points/obj and paste in your UUIDs   http://127.0.0.1:5000/api/1.1/device/points/obj/d0554857-47df-4100-bf6c-43deafb9aa88,5430510a-f0d9-49be-abcc-ddcbf35eb21b
```
