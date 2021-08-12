from logging import StreamHandler


class MqttStreamHandler(StreamHandler):

    def emit(self, record):
        from src.services.mqtt_client import MqttClient
        msg = self.format(record)
        MqttClient.publish_debug(msg)
