#!/bin/bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python3-pip python3-pip virtualenv -y
pip install -U pip setuptools wheel
rm -r venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
sudo cp systemd/nubeio-bac-rest.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nubeio-bac-rest.service
sudo systemctl start nubeio-bac-rest.service
