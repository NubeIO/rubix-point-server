from src.utils import Singleton


class MqttRegistry(metaclass=Singleton):

    def __init__(self):
        self.__mqtt_clients = []

    def clients(self):
        return self.__mqtt_clients

    def add(self, client):
        if client:
            self.__mqtt_clients.append(client)
