# CHANGELOG
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
