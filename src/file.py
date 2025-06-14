import re


def is_bytes(data):
    return data.find(b'\x02') > -1 and data.find(b'\x03') > -1


def is_hex_string(data):
    return data.find(b'02') > -1 and data.find(b'03') > -1


def string_to_binary(data_string):
    data_text = data_string.strip()
    data = ''
    for idx in range(0, len(data_text), 2):
        char = data_text[idx: idx + 2]
        num = int(char, 16)
        data += chr(num)
    return data.encode()


def get_messages(data):
    if is_hex_string(data):
        return list(map(lambda msg: [string_to_binary(msg)], data.splitlines()))
    elif is_bytes(data):
        return re.findall(rb'\x02.+?\x03.', data)
    else:
        raise RuntimeError('No valid messages found')
