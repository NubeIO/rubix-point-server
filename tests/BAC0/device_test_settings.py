


network = {
    'network_ip':'192.168.0.100',
    'network_mask': 24,
    'network_port': 47808,
    'network_device_id': 22,
    'network_device_name': 'whats up',
    'network_number': '24',
}

net_url = f"{network['network_ip']}/{network['network_mask']}:{network['network_port']}"




test_device = {
    'network_ip':'192.168.0.202',
    'network_mask': 24,
    'network_port': 47808,
    'network_device_id': 202,
    'network_device_name': 'whats up12',
}

test_device_url = f"{test_device['network_ip']}/{test_device['network_mask']}:{test_device['network_port']}"



test_device_id = test_device['network_device_id']




