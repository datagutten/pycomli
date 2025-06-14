import re
import struct

from utils import hex_string


def checksum(message):
    check = 0
    for byte in message:
        check ^= byte
    return check


def convert_data(message):
    if not message:
        return None
    reverse = message[::-1]
    converted = ''
    for byte in reverse:
        byte_hex = '%x' % byte
        if byte <= 0x0f:
            byte_hex = '0%s' % byte_hex
        converted += byte_hex
    return int(converted, 16)


def parse_multi(data_multi, base_address=0):
    messages = {}
    offset = 0
    for idx in range(0, len(data_multi), 2):
        char = data_multi[idx: idx + 2]
        if len(char) == 2:
            unpack = struct.unpack('<H', char)
            messages[base_address + offset] = unpack[0]
        else:
            messages[base_address + offset] = convert_data(char)

        offset += 1
    return messages


def get_message_data(message):
    if message[0] != 0x02 or message[-2] != 0x03:
        raise RuntimeError('Invalid message')
    return message[11:-2]


def get_message_header(message):
    return {
        # 'destination': destination,
        'stamp': message[3],
        'message_type': message[4],
        'address': int(message[5:9], 16),
        'quantity': int(message[9:11], 16),
        'checksum': message[-1],
    }


def get_register_range(message):
    headers = get_message_header(message)
    num_registers = int(headers['quantity'] / 2)
    return [headers['address'], headers['address'] + num_registers]


def unpack_value(value):
    """
    >=2 byte = 1 register using binary communication.
    >=4 byte = 1 register using ASCII communication.
    <=64 byte = 32 registers using binary communication.
    >=64 byte = 16 registers using ASCII communication.

    """
    if len(value) == 2:
        return struct.unpack('<H', value)[0]
    elif len(value) == 4:
        return struct.unpack('<L', value)[0]


def parse_message(message):
    if message[0] != 0x02 or message[-2] != 0x03:
        return None
    message_type = message[4]
    if message_type == 81:
        return None

    data_bytes = message[11:-2]

    output = {
        # 'destination': destination,
        'stamp': message[3],
        'message_type': message_type,
        'address': int(message[5:9], 16),
        'quantity': int(message[9:11], 16),
        'checksum': message[-1],
        'message_hex': hex_string(message)
    }
    if message[1:2] == b'\x00':
        output['destination'] = None
    else:
        output['destination'] = int(message[1:2], 16)

    if len(data_bytes) > 0:
        output['data'] = convert_data(data_bytes)
        output['data_hex'] = hex_string(data_bytes)

        if len(data_bytes) > 2:
            output['data_multi'] = parse_multi(message[11:-2], output['address'])
        elif len(data_bytes) == 2:
            output['data_unpack'] = struct.unpack('<H', data_bytes)[0]

    return output


def build_message(address: int, quantity: int, message_type: int = 60, stamp: int = 49, destination: int = 0) -> bytes:
    """
    Build a Comli message
    :param address: Register address
    :param quantity: Number of bytes
    :param message_type: Message type (Usually 60 read RAM or 61 write RAM)
    :param stamp: Message identifier to match the response to the request
    :param destination: Destination device address
    :return: Message with checksum to be sent to a device
    """
    message = b'\x02'
    message += ('%02d' % destination).encode()
    message += stamp.to_bytes(1, 'big')
    message += message_type.to_bytes(1, 'big')
    message += ('%04x' % address).encode()
    message += ('%02d' % quantity).encode()
    message += b'\x03'
    message += checksum(message[1:]).to_bytes(1, 'big')
    return message
