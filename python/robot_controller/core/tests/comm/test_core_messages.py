import unittest

from ...comm.core_messages import CapabilitiesCfm
from ...comm.core_messages import CapabilitiesReq
from ...comm.message_protocol import MessageProtocol
from ...log.log import Log

class TestMessageProtocol(unittest.TestCase):

    def testCapabilitiesCfm(self):
        Log.log("Test")

        testProtocol = MessageProtocol([CapabilitiesReq, CapabilitiesCfm])

        test_msg = CapabilitiesCfm([testProtocol])

        data = test_msg.encode()

        to_verify = CapabilitiesCfm()

        to_verify.decode(data)

        self.assertEqual(test_msg.msg_ids, to_verify.msg_ids)