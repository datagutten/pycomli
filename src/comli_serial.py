import serial
import comli


def trim_message(message):
    start = message.find(b'\x02')
    end = message.find(b'\x03')
    return message[start:end + 2]


def get_data(address, quantity):
    request = comli.build_message(address, quantity, destination=24)
    sent = ser.write(request)
    response = ser.read(128)
    with open('response_%d_%d' % (address, quantity), 'wb') as fp:
        fp.write(response)
    response_parsed = comli.parse_message(trim_message(response))
    return response_parsed['data']


ser = serial.Serial('COM1', parity=serial.PARITY_EVEN, timeout=5)
print(ser.name)


try:
    print('Device has %d DI' % get_data(0x14, 16))
except TypeError:
    pass
try:
    print(get_data(21000, 32))
except TypeError:
    pass