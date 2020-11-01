

'''
Based on: http://www.syxthsense.com/product/product_pdf/MOD3.102-SRI-70.pdf
Room Controller
Simulates and queries device based on the above data sheet.
'''


def run_application() -> str:
    '''
    Simulate and query the device.
    :return: Object query result.
    '''

    from tests.bacnet.bac_server_test import SimulateAndQueryDeviceApplication

    return SimulateAndQueryDeviceApplication.run_application(objectIdentifier=20, objectName="SRI70_001", objectType=8,
                                                             systemStatus='operational', vendorName='SyxthSense Ltd',
                                                             vendorIdentifier=651, modelName='SRI7', protocolVersion=1,
                                                             protocolRevision=10, maxapdulength=480,
                                                             segmentationSupported="noSegmentation",
                                                             apduTimeout=6000, numberOfApduRetries=3, maxMaster=127)


if __name__ == "__main__":
    print(run_application())