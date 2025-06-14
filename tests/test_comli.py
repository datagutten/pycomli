import unittest
import comli


class TestComli(unittest.TestCase):
    def test_checksum(self):
        data = b'\x30\x30\x31\x3c\x30\x30\x31\x34\x30\x32\x03'
        checksum = comli.checksum(data)
        self.assertEqual(checksum, 9)

    def test_message_checksum(self):
        message = comli.build_message(0x14, 2)
        self.assertEqual(message[-1], 9)

    def test_parse_request(self):
        with open('test_data/read hex14', 'rb') as fp:
            data = fp.read()
            parsed = comli.parse_message(data)
            self.assertEqual(parsed['destination'], 0)
            self.assertEqual(parsed['stamp'], 0x31)
            self.assertEqual(parsed['address'], 0x14)
            self.assertEqual(parsed['quantity'], 2)
            self.assertEqual(parsed['checksum'], 0x09)

    def test_convert_data(self):
        out = comli.convert_data(b'\x00\x50')
        self.assertEqual(out, 20480)


if __name__ == '__main__':
    unittest.main()
