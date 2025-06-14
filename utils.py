def hex_string(value):
    converted = ''
    for byte in value:
        byte_hex = '%x' % byte
        if byte <= 0x0f:
            byte_hex = '0%s' % byte_hex
        converted += byte_hex
    return converted
