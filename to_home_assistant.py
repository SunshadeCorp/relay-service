#!/usr/bin/env python3
import yaml


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def to_home_assistant():
    with open('config.yaml', 'r') as file:
        try:
            content = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)
            return
    target_list = []
    for relay_number in content['relays']:
        relay = content['relays'][relay_number]
        target_list.append({
            'platform': 'mqtt',
            'command_topic': f'master/relays/{relay_number}/set',
            'state_topic': f'master/relays/{relay_number}',
            'payload_off': 'off',
            'payload_on': 'on',
            'name': relay['name'],
            'unique_id': f'relay.{relay_number}',
        })
    with open('mqtt_relay_switches.yaml', 'w', encoding='utf8') as outfile:
        yaml.dump(target_list, outfile, default_flow_style=False)
    dump = yaml.dump(target_list, Dumper=MyDumper, default_flow_style=False)
    print(dump)


if __name__ == '__main__':
    to_home_assistant()
