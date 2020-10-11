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
	uuid TEXT NOT NULL,
	mac INTEGER NOT NULL,
	bac_device_id INTEGER NOT NULL,
	ip INTEGER NOT NULL,
	mask INTEGER NOT NULL,
    port INTEGER NOT NULL,
	network_uuid TEXT NOT NULL,
	FOREIGN KEY (network_uuid) REFERENCES networks(uuid)
);
 
DROP TABLE networks

CREATE TABLE networks (
	id INTEGER PRIMARY KEY,
	uuid TEXT NOT NULL,
	ip INTEGER NOT NULL,
	mask INTEGER NOT NULL,
	port INTEGER NOT NULL,
	network_number INTEGER NOT NULL
);
  
```
