import unittest

import paho.mqtt.client as mqtt

from mosquitto_server import MosquittoServer
from service import GpioService


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.mosquitto_server = MosquittoServer()
        self.mosquitto_server.run_as_daemon()

        self.gpio_service = GpioService(relay_config=GpioService.get_config())
        self.gpio_service.loop_as_daemon()

    def test_something(self):
        self.assertEqual(True, False)

    def test_send_message(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host='127.0.0.1', port=1883, keepalive=60)
        for relay_number in self.gpio_service.relays:
            self.mqtt_client.publish(f'master/relays/{relay_number}/set')
        self.mqtt_client.disconnect()


if __name__ == '__main__':
    unittest.main()
