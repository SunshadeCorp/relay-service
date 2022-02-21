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
    target_dict = {'switch': []}
    for relay_number in content['relays']:
        target_dict['switch'].append({
            'platform': 'mqtt',
            'command_topic': f'master/relays/{relay_number}/set',
            'payload_off': 'off',
            'payload_on': 'on',
            'state_topic': f'master/relays/{relay_number}',
            'unique_id': f'relay.{relay_number}',
            'name': f"{content['relays'][relay_number]['name']}",
        })
    dump = yaml.dump(target_dict, Dumper=MyDumper, default_flow_style=False)
    dump = dump.replace('\\xC2\\xB0C', '\\xB0C')
    print(dump)


if __name__ == '__main__':
    to_home_assistant()
