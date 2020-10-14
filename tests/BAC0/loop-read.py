# import BAC0

# from device_test_settings import  test_device_url, net_url, test_device, test_device_id



# bacnet = BAC0.lite(ip=net_url)

# my_obj_list = [
#              ('analogInput', 2),
#              ('analogInput', 3),
#              ('analogInput', 5),
#              ('analogInput', 4),
#              ('analogInput', 1)]

# print(bacnet)
# print(my_obj_list)
# print(test_device_id)

# device = BAC0.device(test_device_url, test_device_id, bacnet, object_list = my_obj_list )

# print(device)
# device.points
# device['point_name']


import BAC0
import time

def polling():

    bacnet = BAC0.connect(ip='192.168.0.100')
    object_list= [('analogInput', 1), ('analogInput', 2)]

    # I tried both ways of changing the poll delay
    device = BAC0.device('192.168.0.202', 202, bacnet, object_list=object_list, poll=1)
    # device['flowTemperature'].poll(delay=1)

    # device.update_history_size(100)
    # device.clear_histories()

    for i in range(5):
        time.sleep(1)

    # print(device['flowTemperature'].history)

if __name__ == '__main__':
    polling()