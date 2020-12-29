# Rubix Point Server

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-point --clean --onefile --add-data VERSION:VERSION
    ```

  The output is: `dist/rubix-point`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-point:dev`

### Run

```bash
docker volume create rubix-point-data
docker run --rm -it -p 1515:1515 -v rubix-point-data:/data --name rubix-point rubix-point:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ rubix-point -h
Usage: rubix-point [OPTIONS]

Options:
  -p, --port INTEGER              Port  [default: 1515]
  -d, --data-dir PATH             Application data dir
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix-Point: setting json file
  -l, --logging-conf TEXT         Rubix-Point: logging config file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  -c, --gunicorn-config TEXT      Gunicorn: config file(gunicorn.conf.py)
  --log-level [FATAL|ERROR|WARN|INFO|DEBUG]
                                  Logging level
  -h, --help                      Show this message and exit.
```


## DOCS
___
### Config

#### Development
```bash
cp config/config.example.json config/config.json

python run.py -s config/config.json
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
