# @Time    : 2018/4/8 13:48
# @Author  : Niyoufa
import unittest
from microserver.tests import print_testcase
from microserver.libs.constlib import const
from microserver.libs.constlib import ConstCaseError, ConstError


class ConstTestCase(unittest.TestCase):

    def setUp(self):
        const.A = 0
        const.A_B = 1

    def tearDown(self):
        const.__delattr__("A")
        const.__delattr__("A_B")

    @print_testcase
    def test_setattr(self):
        with self.assertRaises(ConstCaseError):
            const.a = ""

        with self.assertRaises(ConstError):
            const.A = 0

        with self.assertRaises(ConstError):
            const.A_B = 0

    @print_testcase
    def test_getattr(self):
        self.assertEqual(const.A, 0)
        self.assertEqual(const.A_B, 1)


if __name__ == "__main__":
    unittest.main()
