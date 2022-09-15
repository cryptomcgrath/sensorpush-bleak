import unittest
import utils as ut

class UtilsTestCase(unittest.TestCase):

    def test_hexStrToInt(self):
        self.assertEqual(ut.hexStrToInt("0a cd"), 52490)
        self.assertEqual(ut.hexStrToInt("0acd"), 52490)

    def test_hexStrToByteArray(self):
        self.assertEqual(ut.hexStrToBytes("0a cd"), bytearray(b'\x0a\xcd'))

    def test_intToHexStr(self):
        self.assertEqual(ut.intToHexStr(52490), "0acd0000")


