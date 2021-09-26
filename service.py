#!/usr/bin/env python3
import threading
from pathlib import Path
from threading import Lock
from time import sleep
from typing import Dict, Any

import paho.mqtt.client as mqtt
import yaml
from gpiozero import DigitalOutputDevice, BadPinFactory, DigitalInputDevice

from virtual_digital_output_device import VirtualDigitalOutputDevice


class Relay:
    def __init__(self, number: int, client: mqtt.Client, pin: int, name: str):
        self.number = number
        self.client = client
        self.pin = pin
        self.name = name
        try:
            self.output = DigitalOutputDevice(self.pin)
        except BadPinFactory as e:
            print(f'{e}')
            self.output = VirtualDigitalOutputDevice(self.pin)

    @classmethod
    def from_dict(cls, number: int, client: mqtt.Client, relay_dict: Dict):
        return cls(number, client, relay_dict[number]['pin'], relay_dict[number]['name'])

    def on(self):
        if not self.is_active():
            self.output.on()
        self.publish_state()

    def off(self):
        if self.is_active():
            self.output.off()
        self.publish_state()

    def is_active(self):
        return self.output.is_active

    def state(self) -> str:
        return 'on' if self.is_active() else 'off'

    def publish_state(self):
        self.client.publish(f'master/relays/{self.number}', self.state())

    def subscribe(self):
        self.client.subscribe(f'master/relays/{self.number}/set')
        self.client.subscribe(f'master/relays/{self.number}/status')


class GpioService:
    def __init__(self, relay_config: Dict):
        self.relays = relay_config['relays']
        self.precharge_lock = Lock()
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_message = self.mqtt_on_message

        self.kill_switch = DigitalInputDevice(relay_config['kill_switch']['pin'], pull_up=False, bounce_time=0.1)
        self.kill_switch.when_activated = self.kill_switch_pressed
        self.kill_switch.when_deactivated = self.kill_switch_released

        for relay_number in self.relays:
            self.relays[relay_number] = Relay.from_dict(relay_number, self.mqtt_client, self.relays)

        self.mqtt_client.connect(host='127.0.0.1', port=1883, keepalive=60)

    def kill_switch_pressed(self):
        for relay_number in self.relays:
            self.relays[relay_number].off()
        self.mqtt_client.publish('master/relays/kill_switch', 'pressed')

    def kill_switch_released(self):
        self.mqtt_client.publish('master/relays/kill_switch', 'released')

    @staticmethod
    def get_config() -> Dict:
        with open(Path(__file__).parent / 'config.yaml', 'r') as file:
            try:
                config = yaml.safe_load(file)
                print(config)
                return config
            except yaml.YAMLError as e:
                print(e)

    def loop(self):
        self.mqtt_client.loop_forever(retry_first_connection=True)

    def loop_as_daemon(self):
        self.mqtt_client.loop_start()

    def mqtt_on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict, rc: int):
        for relay_number in self.relays:
            self.relays[relay_number].subscribe()
            self.relays[relay_number].publish_state()
        self.mqtt_client.subscribe('master/relays/precharge')
        self.mqtt_client.publish('master/relays/kill_switch', 'pressed' if self.kill_switch.is_active else 'released')

    def precharge(self):
        if not self.precharge_lock.locked():
            with self.precharge_lock:
                if 1 in self.relays and 2 in self.relays and 3 in self.relays:
                    if not self.relays[1].is_active() \
                            and not self.relays[2].is_active() \
                            and not self.relays[3].is_active():
                        self.relays[2].on()
                        sleep(1)
                        self.relays[3].on()
                        sleep(5)
                        self.relays[1].on()
                        sleep(0.5)
                        self.relays[3].off()
                    if self.kill_switch.is_active:
                        self.kill_switch_pressed()

    def mqtt_on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
        if msg.topic.startswith('master/relays/'):
            relay_number = msg.topic[msg.topic.find('/') + 1:msg.topic.rfind('/')]
            relay_number = relay_number[relay_number.find('/') + 1:]
            if relay_number.isnumeric():
                relay_number = int(relay_number)
                if relay_number in self.relays:
                    if msg.topic.endswith('/set') and len(msg.payload) > 0:
                        payload = msg.payload.decode()
                        if payload.lower() == 'on':
                            self.relays[relay_number].on()
                        elif payload.lower() == 'off':
                            self.relays[relay_number].off()
                    elif msg.topic.endswith('/status'):
                        self.relays[relay_number].publish_state()
            if msg.topic == 'master/relays/precharge':
                threading.Thread(name='precharge', target=self.precharge).start()


if __name__ == '__main__':
    gpio_service = GpioService(relay_config=GpioService.get_config())
    gpio_service.loop()
