import unittest
from ...log.log import Log
from ...comm.message_protocol import MessageProtocol
from ...comm.message_base import MessageBase
import struct

class TestMessage(MessageBase):
    val = 1000

    @staticmethod
    def get_msg_id():
        return 37

    def encode(self):
        return struct.pack('<h', TestMessage.val)

    def decode(self, data):
        self.payload = struct.unpack('<h', data)[0]

class TestMessageProtocol(unittest.TestCase):
    def setUp(self):
        Log.log_file_name = "test_message_protocol.log"

    def test_encode(self):
        protocol = MessageProtocol([TestMessage])
        message = TestMessage()
        data = protocol.encode_message(message)
        received_message = protocol.decode_message(data)

        self.assertEqual(received_message.get_msg_id(), message.get_msg_id())
        self.assertEqual(received_message.val, message.val)

if __name__ == '__main__':
    unittest.main()