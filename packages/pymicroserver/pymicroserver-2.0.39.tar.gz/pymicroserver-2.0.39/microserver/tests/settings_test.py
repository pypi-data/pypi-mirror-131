# @Time    : 2018/4/9 13:47
# @Author  : Niyoufa
import os
import unittest
import importlib
from microserver.tests import print_testcase
from microserver.libs.constlib import ConstError
from microserver.conf import settings


class SettingsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @print_testcase
    def test_getattr(self):
        default_settings = importlib.import_module(os.environ.get("SETTINGS_MODULE"))
        for const in dir(default_settings):
            if const.isupper():
                self.assertEqual(getattr(settings, const), getattr(default_settings, const))

        with self.assertRaises(ConstError):
            print(settings.a)

    @print_testcase
    def test_setattr(self):
        with self.assertRaises(ConstError):
            settings.a = 0

    @print_testcase
    def test_static_absolute_path(self):
        static_absolute_path = settings.get_static_absolute_path()
        self.assertEqual(static_absolute_path,
                         os.path.join(settings.BASE_DIR, "static"))

    @print_testcase
    def test_template_absolute_path(self):
        template_absolute_path = settings.get_template_absolute_path()
        self.assertEqual(template_absolute_path,
                         os.path.join(settings.BASE_DIR, "templates"))
