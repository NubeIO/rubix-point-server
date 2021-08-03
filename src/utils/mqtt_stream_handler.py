from logging import StreamHandler


class MqttStreamHandler(StreamHandler):

    def emit(self, record):
        from src.services.mqtt_client import MqttClient, MqttRegistry

        for client in MqttRegistry().clients():
            if client.config and client.config.publish_debug:
                try:
                    msg = self.format(record)
                    MqttClient.publish_debug(msg)
                except Exception as e:
                    MqttClient.publish_debug(str(e))
