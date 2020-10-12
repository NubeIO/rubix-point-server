# BACnet rest-api

dev in py 3.7

```bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python3-pip virtualenv -y
pip install -U pip setuptools wheel
rm -r venv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app.py
flask run
```

```
# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()
```

# Run Server (http://localhst:5000)
python app.py

Had to update the BBB from 3.5 to 3.7 but didn't work

```bash
sudo apt update
sudo apt install software-properties-common
## had issue on install and needed to install this
sudo apt-get install dirmngr
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7

```



```sql
 
DROP TABLE devices

CREATE TABLE devices (
	id INTEGER PRIMARY KEY,
	bac_device_uuid TEXT NOT NULL,
	bac_device_mac INTEGER NOT NULL,
	bac_device_id INTEGER NOT NULL,
	bac_device_ip INTEGER NOT NULL,
	bac_device_mask INTEGER NOT NULL,
    bac_device_port INTEGER NOT NULL,
	network_uuid TEXT NOT NULL,
	 FOREIGN KEY (network_uuid)
       REFERENCES networks (network_uuid) 
);
 
DROP TABLE networks

CREATE TABLE networks (
	id INTEGER PRIMARY KEY,
	network_uuid TEXT NOT NULL,
	network_ip INTEGER NOT NULL,
	network_mask INTEGER NOT NULL,
	network_port INTEGER NOT NULL,
	network_number INTEGER NOT NULL,
	network_device_id INTEGER NOT NULL,
	network_device_name TEXT NOT NULL,
);
  
SELECT * FROM networks
SELECT * FROM devices 
  
```
