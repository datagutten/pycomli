"""
Parse Comli messages from a file and dump to json
"""
import comli
import json
import re
import sys

messages_parsed = []

with open(sys.argv[1], 'rb') as fp:
    data = fp.read()
    if data.find(b'\x02') == data.find(b'\x03') == -1 and data.find(b'02') > -1 and data.find(b'03'):
        # messages = comli.string_to_binary(data).splitlines()
        messages = list(map(lambda msg: [comli.string_to_binary(msg)], data.splitlines()))
    else:
        messages = re.findall(rb'(\x02(.+?)\x03(.))', data)
    for message in messages:
        info = comli.parse_message(message[0])
        messages_parsed.append(info)
with open(sys.argv[1] + '.json', 'w') as fp:
    json.dump(messages_parsed, fp, indent=2)
