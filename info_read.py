import json

import file, comli

with open('registers/myconnect.json') as fp:
    registers = json.load(fp)
values = {}
with open('tests/test_data/read register 51', 'rb') as fp:
    data = fp.read()
    message = file.get_messages(data)[0]
    header = comli.get_message_header(message)
    data_bytes = comli.get_message_data(message)
    data_bytes_hex = comli.hex_string(data_bytes)
    first_register, last_register = comli.get_register_range(message)

    for register in range(first_register, last_register + 1):
        pos = register - first_register

        if str(register) in registers:
            info = registers[str(register)]
            end_pos = pos + info['length'] * 2
            data2 = data_bytes[pos:end_pos]
            print('Read %d bytes for %s' % (len(data2), info['name']))
            value = comli.unpack_value(data2)
            values[info['name']] = value

    pass
