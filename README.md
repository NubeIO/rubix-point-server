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
    poetry run pyinstaller run.py -n rubix-point --clean --onefile \
        --add-data VERSION:. \
        --add-data config:config
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
  -g, --global-dir PATH           Global dir
  -d, --data-dir PATH             Application data dir
  -c, --config-dir PATH           Application config dir
  --prod                          Production mode
  -s, --setting-file TEXT         Rubix Point: setting json file
  -l, --logging-conf TEXT         Rubix Point: logging config file
  --workers INTEGER               Gunicorn: The number of worker processes for handling requests.
  --gunicorn-config TEXT      Gunicorn: config file(gunicorn.conf.py)
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
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/<event>/...
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/<all|value>/<Drivers>/<network_uuid>/<network_name>/<device_uuid>/<device_name>/<point_uuid>/<point_name>
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/model/<ModelEvent>/<model.uuid>
```
```
COV:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/all/<driver>/<network_uuid>/<network_name>/<device_uuid>/<device_name>/<point_uuid>/<point_name>

  [optional] (value only)
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/value/<driver>/<network_uuid>/<network_name>/<device_uuid>/<device_name>/<point_uuid>/<point_name>

MODEL:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/model/<model>/<model.uuid>
```

Debug topic
```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/debug
```

Debug topic example
```
+/+/+/+/+/+/rubix/points/debug
```

#### Example topics:

**COV:**
```
all points:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/all/#

all modbus rtu points:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/all/modbus/+/+/+/+/+/+

by point uuid:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/all/+/+/+/+/+/<point_uuid>/+

by point name:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/cov/all/+/+/<network_name>/+/<device_name>/+/<point_name>
```
**MODEL:**
```
network:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/model/network/example_network_uuid

device:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/model/device/example_device_uuid

point:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/model/point/example_point_uuid

points list:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/points
  
schedule list:
  <client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/schedules
```

### Generic Points MQTT Listener

- All generic point values are updated over MQTT
- These COVs are then broadcast again over the normal MQTT clients as above

#### Topic structure:

```
<client_id>/<site_id>/<device_id>/rubix/points/listen/cov/name/<point_name>/<device_name>/<network_name>
<client_id>/<site_id>/<device_id>/rubix/points/listen/cov/uuid/<point_uuid>
```

### Generic Points List Publisher

```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/points
```

### Schedule List Publisher
```
<client_id>/<client_name>/<site_id>/<site_name>/<device_id>/<device_name>/rubix/points/value/schedules
```
