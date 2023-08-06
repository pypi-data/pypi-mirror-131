# @Time    : 2018/4/9 下午9:09
# @Author  : Niyoufa
import unittest
from microserver.conf import settings
from microserver.tests import print_testcase
from microserver.core.module import ModuleManager, Module
from microserver.core.handlers.handlers import BaseHandler


class ModuleManagerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @print_testcase
    def test_init(self):
        self.assertEqual(id(ModuleManager()), id(ModuleManager()))

        modulemanager = ModuleManager()
        self.assertEqual(len(modulemanager.modules), len(settings.MODULES))
        for module in modulemanager.modules:
            self.assertIsInstance(module, Module)

        handlers = modulemanager.get_handlers()
        self.assertIsInstance(handlers, list)
        for handler in handlers:
            self.assertEqual(issubclass(handler[1], BaseHandler), True)