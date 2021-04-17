# CHANGELOG
## [v1.6.0](https://github.com/NubeIO/rubix-point-server/tree/v1.6.0) (2020-04-18)
### Added
- Tag Keys should support camel case
- Modbus On point write dont poll write value again 

## [v1.5.9](https://github.com/NubeIO/rubix-point-server/tree/v1.5.9) (2020-04-12)
### Added
- Fix: math apply_scale function
- Added tags to devices and networks
- Update to apply math function
- Fix: MQTT network retain clear issue
- Fix: ModbusFunctionCode issue (Invalid function code)
- Improvement: generic point priority array write on update


## [v1.5.8](https://github.com/NubeIO/rubix-point-server/tree/v1.5.8) (2020-04-02)
### Added
- Fix: multiple r/w
- Miscellaneous improvements on code

## [v1.5.7](https://github.com/NubeIO/rubix-point-server/tree/v1.5.7) (2020-03-31)
### Added
- Fix: write value issue (priority_array addition support)

## [v1.5.6](https://github.com/NubeIO/rubix-point-server/tree/v1.5.6) (2020-03-26)
### Added
- Process MQTT message on different process

## [v1.5.5](https://github.com/NubeIO/rubix-point-server/tree/v1.5.5) (2020-03-26)
### Added
- Fix: Listener retain msg clearing issue
- Don't clear schedule listener value
- Add schedule resource by name

## [v1.5.4](https://github.com/NubeIO/rubix-point-server/tree/v1.5.4) (2020-03-24)
### Added
- Fix: priority array patch on point model

## [v1.5.3-r1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.3-r1) (2020-03-22)
### Added
- Fix: write_analogue issue fix (should be an integer) on v1.5.3

## [v1.5.2-r1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.2-r1) (2020-03-22)
### Added
- Fix: write_analogue issue fix (should be an integer)

## [v1.5.3](https://github.com/NubeIO/rubix-point-server/tree/v1.5.3) (2020-03-21)
### Added
- Add priority array on Modbus points
- Modbus value writer for writable points
- Sync points mappings issues fixes
- Change API from `/api/mp_gbp/mappings` to `/api/mappings/mp_gbp`

## [v1.5.2](https://github.com/NubeIO/rubix-point-server/tree/v1.5.2) (2020-03-19)
### Added
- Modbus polling poll aggregation
- schedules api
- Model publish improvement over MQTT

## [v1.5.1](https://github.com/NubeIO/rubix-point-server/tree/v1.5.1) (2020-03-13)
### Added
- Modbus polling loop remove on network deletion
- Support for Generic Point payload write

## [v1.5.0](https://github.com/NubeIO/rubix-point-server/tree/v1.5.0) (2020-03-11)
### Added
- Publish points uuid list on MQTT
- Removed out generic listener and adding that functionality on MqttClient
- Update generic point_store value by MQTT name or uuid request
- Use MQTT flags on MQTT data publish
- Don't give retain option to user (we standardize it, retain True on values, models publish and False on debug)
- Clear retain values and listen values (we can only have valid topic with retain True)
- Resubscribe on certain interval to clear values (it clears no more invalid topics, and frontend won't have much data when subscribing)

## [v1.4.6](https://github.com/NubeIO/rubix-point-server/tree/v1.4.6) (2020-03-11)
### Added
- Fix: modbus ping point

## [v1.4.5](https://github.com/NubeIO/rubix-point-server/tree/v1.4.5) (2020-03-09)
### Added
- Fix: same network can't have multiple devices
- Don't publish value on MQTT when PATCH did nothing change

## [v1.4.4-rc1](https://github.com/NubeIO/rubix-point-server/tree/v1.4.4-rc1) (2020-03-09)
### Added
- Convert drivers list values to enum
- Rename package source_drivers to drivers
- Rename interfaces to enums
- Polling improvements
- Device enable model change to boolean from string

## [v1.4.3](https://github.com/NubeIO/rubix-point-server/tree/v1.4.3) (2020-03-04)
### Added
- Postgres sync update & tags addition

## [v1.4.2](https://github.com/NubeIO/rubix-point-server/tree/v1.4.2) (2020-03-03)
### Added
- Upgrade mqtt-rest-bridge (listener issue fix)
- Separate data and config files

## [v1.4.1](https://github.com/NubeIO/rubix-point-server/tree/v1.4.1) (2020-03-03)
### Added
- Runtime values edition reflect

## [v1.4.0](https://github.com/NubeIO/rubix-point-server/tree/v1.4.0) (2020-03-02)
### Added
- Added in time-delay between points on modbus polling

## [v1.3.9](https://github.com/NubeIO/rubix-point-server/tree/v1.3.9) (2020-03-01)
### Added
- COV point store issue fix

## [v1.3.8](https://github.com/NubeIO/rubix-point-server/tree/v1.3.8) (2020-02-26)
### Added
- Priority array write issue fix

## [v1.3.7](https://github.com/NubeIO/rubix-point-server/tree/v1.3.7) (2020-02-25)
### Added
- Improvement on MQTT code bases (made debug topic standard)

## [v1.3.6](https://github.com/NubeIO/rubix-point-server/tree/v1.3.6) (2020-02-22)
### Added
- Upgrade rubix-http version

## [v1.3.5](https://github.com/NubeIO/rubix-point-server/tree/v1.3.5) (2020-02-22)
### Added
- Add postgresql history sync
- Priority array writer payload change
- Edit/Add APIs for uuid, name services
- Insert validation on network, device, point name
- Add Rubix Registry & remove wires-plat
- Standardize publish MQTT topic
- Implement rubix-http for standardizing HTTP error msg

## [v1.3.4](https://github.com/NubeIO/rubix-point-server/tree/v1.3.4) (2020-02-16)
### Added
- Updates to protocal-brige

## [v1.3.3](https://github.com/NubeIO/rubix-point-server/tree/v1.3.3) (2020-02-15)
### Added
- Updates to protocal-brige

## [v1.3.2](https://github.com/NubeIO/rubix-point-server/tree/v1.3.2) (2020-02-09)
### Added
- MQTT REST bridge listener name change (issue fix on conflict)
- Polling status addition on ping service

## [v1.3.1](https://github.com/NubeIO/rubix-point-server/tree/v1.3.1) (2020-02-09)
### Added
- MQTT REST bridge integration & Generic Point <> BACnet Point sync service
- Fields addition on `generic_points` (`type`, `unit`)  

## [v1.3.0](https://github.com/NubeIO/rubix-point-server/tree/v1.3.0) (2020-02-03)
### Added
- Add auth for mqtt and ssl for influx
- Add Priority Array on Points

## [v1.2.9](https://github.com/NubeIO/rubix-point-server/tree/v1.2.9) (2020-02-01)
### Added
- Add tags for influxdb on generic points

## [v1.2.8](https://github.com/NubeIO/rubix-point-server/tree/v1.2.8) (2020-01-29)
### Added
- Add HTTP PATCH to generic point by name
- fix some modbus polling bugs

## [v1.2.7](https://github.com/NubeIO/rubix-point-server/tree/v1.2.7) (2020-01-28)
### Added
- Add HTTP PATCH to generic point

## [v1.2.6](https://github.com/NubeIO/rubix-point-server/tree/v1.2.6) (2020-01-28)
### Added
- Fixes to influx-db connection

## [v1.2.5](https://github.com/NubeIO/rubix-point-server/tree/v1.2.5) (2020-01-19)
### Added
- Added mqtt debug logs

## [v1.2.4](https://github.com/NubeIO/rubix-point-server/tree/v1.2.4) (2020-01-18)
### Added
- Added new endpoint for calling all devices without returning their points

## [v1.2.3](https://github.com/NubeIO/rubix-point-server/tree/v1.2.3) (2020-01-15)
### Added
- Fix point patch issue

## [v1.2.2](https://github.com/NubeIO/rubix-point-server/tree/v1.2.2) (2020-01-14)
### Added
- Fix to mqtt fault payloads

## [v1.2.1](https://github.com/NubeIO/rubix-point-server/tree/v1.2.1) (2020-01-12)
### Added
- Fix to mqtt and threads

## [v1.2.0](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0) (2020-12-29)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Dockerize
- Change setting file format from `.ini` to `.json`

## [v1.2.0-rc.2](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0-rc.2) (2020-12-28)
### Changed
- Change setting file format from `.ini` to `.json`


## [v1.2.0-rc.1](https://github.com/NubeIO/rubix-point-server/tree/v1.2.0-rc.1) (2020-12-28)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting.conf format
- Dockerize
