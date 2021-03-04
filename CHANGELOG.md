# CHANGELOG
## [v1.4.3](https://github.com/NubeIO/rubix-point-server/tree/v1.4.2) (2020-03-04)
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
