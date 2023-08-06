# @Time    : 2018/4/9 下午8:19
# @Author  : Niyoufa
import unittest
from microserver.tests import print_testcase
from microserver.core.module import Module
from microserver.core.module import ModuleNotExistsError
from microserver.core.handlers.handlers import BaseHandler


class ModuleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @print_testcase
    def test_init(self):
        with self.assertRaises(ModuleNotExistsError):
            Module("xxx")

        module = Module("microserver.addons.siege.handlers")
        self.assertIsInstance(module.handlers, list)

        for handler in module.handlers:
            self.assertEqual(issubclass(handler[1], BaseHandler), True)