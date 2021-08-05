from typing import List

from src.services.mqtt_client import MqttClient
from src.utils import Singleton


class MqttRegistry(metaclass=Singleton):

    def __init__(self):
        self.__mqtt_clients: List[MqttClient] = []

    def clients(self) -> List[MqttClient]:
        return self.__mqtt_clients

    def add(self, client):
        if client:
            self.__mqtt_clients.append(client)
