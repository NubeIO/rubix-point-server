# CHANGELOG
## [v2.1.2](https://github.com/NubeIO/rubix-point-server/tree/v2.1.2) (2022-04-10)
- Fix: Too many open files issues

## [v2.1.0](https://github.com/NubeIO/rubix-point-server/tree/v2.1.0) (2022-01-21)
- Improvement on history_persistency
  - Changed from rows to hours
- Fix: exception handler is not showing error logs

## [v2.1.0](https://github.com/NubeIO/rubix-point-server/tree/v2.1.0) (2022-01-21)
- MQTT SSL support

## [v2.0.8](https://github.com/NubeIO/rubix-point-server/tree/v2.0.8) (2021-12-03)
- Schedule issue fix: it was sending dictionary instead of JSON

## [v2.0.7](https://github.com/NubeIO/rubix-point-server/tree/v2.0.7) (2021-09-20)
- Improvement on MQTT data push (don't send any data when MQTT disable is ON)

## [v2.0.6](https://github.com/NubeIO/rubix-point-server/tree/v2.0.6) (2021-08-27)
- Fix fallback_value migration

## [v2.0.5](https://github.com/NubeIO/rubix-point-server/tree/v2.0.5) (2021-08-19)
- Change buster to slim-buster

## [v2.0.4](https://github.com/NubeIO/rubix-point-server/tree/v2.0.4) (2021-08-19)
- Fallback should be able to set to be null

## [v2.0.3](https://github.com/NubeIO/rubix-point-server/tree/v2.0.3) (2021-08-17)
- Fix: PostgreSQL reconnection issue

## [v2.0.2](https://github.com/NubeIO/rubix-point-server/tree/v2.0.2) (2021-08-16)
- Improvement on PostgreSQL and Influx history sync (don't query much to server)

## [v2.0.1](https://github.com/NubeIO/rubix-point-server/tree/v2.0.1) (2021-08-12)
- Fix: MQTT data push

## [v2.0.0](https://github.com/NubeIO/rubix-point-server/tree/v2.0.0) (2021-08-11)
- Remove modbus and extract it into it's own repo

## [v1.9.1](https://github.com/NubeIO/rubix-point-server/tree/v1.9.1) (2021-07-19)
- Improvement on update_mapping_state (update uuid if name matches on mapping)
- Optimize time on rubix-point value PATCH

## [v1.9.1](https://github.com/NubeIO/rubix-point-server/tree/v1.9.1) (2021-07-19)
- Fix: write value once

## [v1.9.0](https://github.com/NubeIO/rubix-point-server/tree/v1.9.0) (2021-07-16)
- Refactor point mappings

## [v1.8.0](https://github.com/NubeIO/rubix-point-server/tree/v1.8.0) (2021-06-24)
- Upgrade rubix-registry to v1.1.1 (breaking change, use `rubix-service >= v1.7.7`)

## [v1.7.7](https://github.com/NubeIO/rubix-point-server/tree/v1.7.7) (2021-06-23)
- Include page size for large point value sync
- Logger improvements on postgresql
- Add sleep on postgres sync (don't make it heavy for single o/p)
- Remove schedule package

## [v1.7.6](https://github.com/NubeIO/rubix-point-server/tree/v1.7.6) (2021-06-22)
- Fix: schedule dispatch JSON (need to sync JSON)

## [v1.7.5](https://github.com/NubeIO/rubix-point-server/tree/v1.7.5) (2021-06-18)
- Fix: COV for Modbus/generic point
- Have priority array support fallback values
- Use shortuuid (uuid4 with URL supporting base57 encoding)
- Issue fix: InfluxDB large data sync (added option batch) (#375)
- Make server schedule available on the local broker (#376)
- Fix: read write point switch (#378) (#379)

## [v1.7.4](https://github.com/NubeIO/rubix-point-server/tree/v1.7.4) (2021-06-04)
- Retry establishing connection on PostgreSQL connection gets down
- Include device and network tags as well on InfluxDB sync

## [v1.7.3](https://github.com/NubeIO/rubix-point-server/tree/v1.7.3) (2021-06-03)
- Add priority to MQTT message
- Issue fix: value were not writing on COV (#324)

## [v1.7.2](https://github.com/NubeIO/rubix-point-server/tree/v1.7.2) (2021-05-25)
- Add field source ('OWN', 'MAPPING') for source filtration

## [v1.7.1](https://github.com/NubeIO/rubix-point-server/tree/v1.7.1) (2021-05-20)
- InfluxDB _get_point_last_sync_id issue fix
- MAX_ROWS for point history cleaner is set to 200
- Change logging files name

## [v1.7.0](https://github.com/NubeIO/rubix-point-server/tree/v1.7.0) (2021-05-17)
- Add COV_AND_INTERVAL history type support
- Include migrations on build

## [v1.6.9](https://github.com/NubeIO/rubix-point-server/tree/v1.6.9) (2021-05-17)
- History interval issue fix #347
- Updated scale function so that if the scaling factors are equal it does nothing
- Add Flask-Migrate #221 (so its does not break the DB on update)

## [v1.6.8](https://github.com/NubeIO/rubix-point-server/tree/v1.6.8) (2021-05-11)
- Include tags for both modbus and generic types
- Improvements on PostgreSQL schemas and value updates

## [v1.6.7](https://github.com/NubeIO/rubix-point-server/tree/v1.6.7) (2021-05-10)
- Default points value update
- Disable MQTT when disable_mqtt=True
- Remove MQTT models publish

## [v1.6.6](https://github.com/NubeIO/rubix-point-server/tree/v1.6.6) (2021-05-05)
- Optimization of point patch and point value patch

## [v1.6.5](https://github.com/NubeIO/rubix-point-server/tree/v1.6.5) (2021-05-04)
- Change automatic tag keys
- Gunicorn worker timeout: 120
- Postgres, InfluxDB sync timer: 5 minutes

## [v1.6.4](https://github.com/NubeIO/rubix-point-server/tree/v1.6.4) (2021-04-30)
- Update scale database schema for postgres added point name and wires-plat time zone

## [v1.6.3](https://github.com/NubeIO/rubix-point-server/tree/v1.6.3) (2021-04-27)
- Update scale database schema for postgres https://github.com/NubeIO/rubix-point-server/pull/318

## [v1.6.2](https://github.com/NubeIO/rubix-point-server/tree/v1.6.2) (2021-04-23)
- Update scale function
- Fix: point patch, value update issue

## [v1.6.1](https://github.com/NubeIO/rubix-point-server/tree/v1.6.1) (2021-04-20)
- Add input and scale min, max validation
- mqtt-rest-bridge replacement with rubix-http
- Cascade delete points mapping
- Add default value for value_operation
- Support both priority_array_write and write value on priority
- Add Unary arithmetic operator

## [v1.6.0](https://github.com/NubeIO/rubix-point-server/tree/v1.6.0) (2021-04-18)
- Tag Keys should support camel case
- Modbus On point write dont poll write value again 

## [v1.5.9](https://github.com/NubeIO/rubix-point-server/tree/v1.5.9) (2021-04-12)
- Fix: math apply_scale function
- Added tags to devices and networks
- Update to apply math function
- Fix: MQTT network retain clear issue
- Fix: ModbusFunctionCode issue (Invalid function code)
- Improvement: generic point priority array write on update


## [v1.5.8](https://github.com/NubeIO/rubix-point-server/tree/v1.5.8) (2021-04-02)
- Fix: multiple r/w
- Miscellaneous improvements on code

## [v1.5.7](https://github.com/NubeIO/rubix-point-server/tree/v1.5.7) (2021-03-31)
- Fix: write value issue (priority_array addition support)

## [v1.5.6](https://github.com/NubeIO/rubix-point-server/tree/v1.5.6) (2021-03-26)
- Process MQTT message on different process

## [v1.5.5](https://github.com/NubeIO/rubix-point-server/tree/v1.5.5) (2021-03-26)
- Fix: Listener retain msg clearing issue
- Don't clear schedule listener value
- Add schedule resource by name

## [v1.5.4](https://github.com/NubeIO/rubix-point-server/tree/v1.5.4) (2021-03-24)
- Fix: priority array patch on point model

## [v1.5.3-r1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.3-r1) (2021-03-22)
- Fix: write_analogue issue fix (should be an integer) on v1.5.3

## [v1.5.2-r1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.2-r1) (2021-03-22)
- Fix: write_analogue issue fix (should be an integer)

## [v1.5.3](https://github.com/NubeIO/rubix-point-server/tree/v1.5.3) (2021-03-21)
- Add priority array on Modbus points
- Modbus value writer for writable points
- Sync points mappings issues fixes
- Change API from `/api/mp_gbp/mappings` to `/api/mappings/mp_gbp`

## [v1.5.2](https://github.com/NubeIO/rubix-point-server/tree/v1.5.2) (2021-03-19)
- Modbus polling poll aggregation
- schedules api
- Model publish improvement over MQTT

## [v1.5.1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.1) (2021-03-13)
- Modbus polling loop remove on network deletion
- Support for Generic Point payload write

## [v1.5.0](https://github.com/NubeIO/rubix-point-server/tree/v1.5.0) (2021-03-11)
- Publish points uuid list on MQTT
- Removed out generic listener and adding that functionality on MqttClient
- Update generic point_store value by MQTT name or uuid request
- Use MQTT flags on MQTT data publish
- Don't give retain option to user (we standardize it, retain True on values, models publish and False on debug)
- Clear retain values and listen values (we can only have valid topic with retain True)
- Resubscribe on certain interval to clear values (it clears no more invalid topics, and frontend won't have much data when subscribing)

## [v1.4.6](https://github.com/NubeIO/rubix-point-server/tree/v1.4.6) (2021-03-11)
- Fix: modbus ping point

## [v1.4.5](https://github.com/NubeIO/rubix-point-server/tree/v1.4.5) (2021-03-09)
- Fix: same network can't have multiple devices
- Don't publish value on MQTT when PATCH did nothing change

## [v1.4.4-rc1](https://github.com/NubeIO/rubix-point-server/tree/v1.4.4-rc1) (2021-03-09)
- Convert drivers list values to enum
- Rename package source_drivers to drivers
- Rename interfaces to enums
- Polling improvements
- Device enable model change to boolean from string

## [v1.4.3](https://github.com/NubeIO/rubix-point-server/tree/v1.4.3) (2021-03-04)
- Postgres sync update & tags addition

## [v1.4.2](https://github.com/NubeIO/rubix-point-server/tree/v1.4.2) (2021-03-03)
- Upgrade mqtt-rest-bridge (listener issue fix)
- Separate data and config files

## [v1.4.1](https://github.com/NubeIO/rubix-point-server/tree/v1.4.1) (2021-03-03)
- Runtime values edition reflect

## [v1.4.0](https://github.com/NubeIO/rubix-point-server/tree/v1.4.0) (2021-03-02)
- Added in time-delay between points on modbus polling

## [v1.3.9](https://github.com/NubeIO/rubix-point-server/tree/v1.3.9) (2021-03-01)
- COV point store issue fix

## [v1.3.8](https://github.com/NubeIO/rubix-point-server/tree/v1.3.8) (2021-02-26)
- Priority array write issue fix

## [v1.3.7](https://github.com/NubeIO/rubix-point-server/tree/v1.3.7) (2021-02-25)
- Improvement on MQTT code bases (made debug topic standard)

## [v1.3.6](https://github.com/NubeIO/rubix-point-server/tree/v1.3.6) (2021-02-22)
- Upgrade rubix-http version

## [v1.3.5](https://github.com/NubeIO/rubix-point-server/tree/v1.3.5) (2021-02-22)
- Add postgresql history sync
- Priority array writer payload change
- Edit/Add APIs for uuid, name services
- Insert validation on network, device, point name
- Add Rubix Registry & remove wires-plat
- Standardize publish MQTT topic
- Implement rubix-http for standardizing HTTP error msg

## [v1.3.4](https://github.com/NubeIO/rubix-point-server/tree/v1.3.4) (2021-02-16)
- Updates to protocal-brige

## [v1.3.3](https://github.com/NubeIO/rubix-point-server/tree/v1.3.3) (2021-02-15)
- Updates to protocal-brige

## [v1.3.2](https://github.com/NubeIO/rubix-point-server/tree/v1.3.2) (2021-02-09)
- MQTT REST bridge listener name change (issue fix on conflict)
- Polling status addition on ping service

## [v1.3.1](https://github.com/NubeIO/rubix-point-server/tree/v1.3.1) (2021-02-09)
- MQTT REST bridge integration & Generic Point <> BACnet Point sync service
- Fields addition on `generic_points` (`type`, `unit`)  

## [v1.3.0](https://github.com/NubeIO/rubix-point-server/tree/v1.3.0) (2021-02-03)
- Add auth for mqtt and ssl for influx
- Add Priority Array on Points

## [v1.2.9](https://github.com/NubeIO/rubix-point-server/tree/v1.2.9) (2021-02-01)
- Add tags for influxdb on generic points

## [v1.2.8](https://github.com/NubeIO/rubix-point-server/tree/v1.2.8) (2021-01-29)
- Add HTTP PATCH to generic point by name
- fix some modbus polling bugs

## [v1.2.7](https://github.com/NubeIO/rubix-point-server/tree/v1.2.7) (2021-01-28)
- Add HTTP PATCH to generic point

## [v1.2.6](https://github.com/NubeIO/rubix-point-server/tree/v1.2.6) (2021-01-28)
- Fixes to influx-db connection

## [v1.2.5](https://github.com/NubeIO/rubix-point-server/tree/v1.2.5) (2021-01-19)
- Added mqtt debug logs

## [v1.2.4](https://github.com/NubeIO/rubix-point-server/tree/v1.2.4) (2021-01-18)
- Added new endpoint for calling all devices without returning their points

## [v1.2.3](https://github.com/NubeIO/rubix-point-server/tree/v1.2.3) (2021-01-15)
- Fix point patch issue

## [v1.2.2](https://github.com/NubeIO/rubix-point-server/tree/v1.2.2) (2021-01-14)
- Fix to mqtt fault payloads

## [v1.2.1](https://github.com/NubeIO/rubix-point-server/tree/v1.2.1) (2021-01-12)
- Fix to mqtt and threads

## [v1.2.0](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0) (2020-12-29)
- **Breaking Changes**: Make delivery artifact as `binary`
- Dockerize
- Change setting file format from `.ini` to `.json`

## [v1.2.0-rc.2](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0-rc.2) (2020-12-28)
- Change setting file format from `.ini` to `.json`


## [v1.2.0-rc.1](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0-rc.1) (2020-12-28)
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting.conf format
- Dockerize
