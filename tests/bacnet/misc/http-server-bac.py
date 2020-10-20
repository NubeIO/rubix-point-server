'''
Based on: https://www.kele.com/Catalog/08%20Gas_Specialty_Sensors/PDFs/CDD3%20BACNET%20WALL%20INSTALLSHEET.pdf
CDD3 BACnet Room Carbon Dioxide Detector.
Simulates and queries device based on the above data sheet.
'''


def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''
    from bacpypes.object import AnalogInputObject, AnalogValueObject, BinaryValueObject, BinaryInputObject
    from tests.bacnet.misc.SimulateAndQueryDeviceApplication import SimulateAndQueryDeviceApplication

    analog_input_objects = \
        [
            AnalogInputObject(
                objectIdentifier=('analogInput', 1),
                objectName='CO2_Level',
                objectType='analogInput',
                presentValue=21,
                description='CO2 Level',
                deviceType='0-2000 ppm CO2 Sensor',
                statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
                eventState='normal',
                reliability='noFaultDetected',
                outOfService=False,
                units='partsPerMillion'
            ), AnalogInputObject(
            objectIdentifier=('analogInput', 2),
            objectName='Relative_Humidity',
            objectType='analogInput',
            presentValue=60,
            description='Relative Humidity',
            deviceType='0-100 %RH Sensor',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            units='percentRelativeHumidity'
        ), AnalogInputObject(
            objectIdentifier=('analogInput', 3),
            objectName='Temperature',
            objectType='analogInput',
            presentValue=19,
            description='Temperature',
            deviceType='0-35 C Temperature Sensor or 32-95 F Temperature Sensor',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            units='degreesCelsius'
        ), AnalogInputObject(
            objectIdentifier=('analogInput', 4),
            objectName='Setpoint_Control',
            objectType='analogInput',
            presentValue=67,
            description='Setpoint Value',
            deviceType='0-100 % Setpoint',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False,
            units='percent'
        )]

    analog_value_objects = [
        AnalogValueObject(
            objectIdentifier=('analogValue', 1),
            objectName='Relay_Setpoint',
            objectType='analogValue',
            presentValue=1000,
            description='Relay Setpoint',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='partsPerMillion'
        ), AnalogValueObject(
            objectIdentifier=('analogValue', 2),
            objectName='Relay_Hysteresis',
            objectType='analogValue',
            presentValue=50,
            description='Relay Hysteresis',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='partsPerMillion'
        ), AnalogValueObject(
            objectIdentifier=('analogValue', 3),
            objectName='Temperature_Offset',
            objectType='analogValue',
            presentValue=50,
            description='Temperature Offset Calibration',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='deltaDegreesFahrenheit'
        ), AnalogValueObject(
            objectIdentifier=('analogValue', 4),
            objectName='Relative_Humidity_Offset',
            objectType='analogValue',
            presentValue=0,
            description='RH Offset Calibration',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='percentRelativeHumidity'
        ), AnalogValueObject(
            objectIdentifier=('analogValue', 5),
            objectName='Sensor_Altitude',
            objectType='analogValue',
            presentValue=50,
            description='CO2 Sensor Altitude',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='feet'
        ), AnalogValueObject(
            objectIdentifier=('analogValue', 6),
            objectName='Display_Modes',
            objectType='analogValue',
            presentValue=50,
            description='CO2 LCD Display Modes',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            outOfService=False,
            units='noUnits'
        )]

    binary_value_objects = [
        BinaryValueObject(
            objectIdentifier=('binaryValue', 1),
            objectName='Override_Switch',
            objectType='binaryValue',
            presentValue=0,
            description='Override Switch',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 2),
            objectName='Auto_Cal_Enable',
            objectType='binaryValue',
            presentValue=1,
            description='Auto Calibration Enable',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        ), BinaryValueObject(
            objectIdentifier=('binaryValue', 3),
            objectName='Fahrenheit',
            objectType='binaryValue',
            presentValue=1,
            description='Fahrenheit (1) or Celsius (0)',
            statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
            eventState='normal',
            reliability='noFaultDetected',
            outOfService=False
        )]

    binary_input_objects = [BinaryInputObject(
        objectIdentifier=('binaryInput', 1),
        objectName='Relay_On',
        objectType='binaryInput',
        presentValue=0,
        description='Relay Status',
        deviceType='Indicates On/Off Status of Relay',
        statusFlags=['inAlarm', 'inAlarm', 'inAlarm', 'inAlarm'],
        eventState='normal',
        reliability='noFaultDetected',
        outOfService=False,
        polarity='normal',
    )]

    objects = analog_input_objects + analog_value_objects + binary_value_objects + binary_input_objects

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=381003, objectName="CDD_CO2_Detector_003",
                                                             objectType=8, systemStatus='operational',
                                                             vendorName='Greystone Energy Systems',
                                                             vendorIdentifier=381, modelName='CDD2A',
                                                             firmwareRevision='1.4', applicationSoftwareVersion='1.0',
                                                             description='Greystone CO2 Detector',
                                                             protocolVersion=1, protocolRevision=7,
                                                             protocolObjectTypesSupported=['analogInput', 'analogValue',
                                                                                           'binaryInput', 'binaryValue',
                                                                                           'device'],
                                                             maxapdulength=128, segmentationSupported="noSegmentation",
                                                             apduTimeout=10000, numberOfApduRetries=3, maxMaster=127,
                                                             maxInfoFrames=1,
                                                             objects=objects)


if __name__ == "__main__":
    print(run_application())
