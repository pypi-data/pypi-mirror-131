# @Time    : 2018/4/8 14:03
# @Author  : Niyoufa
import os
os.environ.setdefault("SETTINGS_MODULE", "microserver.tests.settings.test_settings")
import unittest

TEST_MODULES = [
    # 'microserver.tests.const_test',
    # 'microserver.tests.settings_test',
    # 'microserver.tests.module_test',
    # 'microserver.tests.modulemanager_test',
    'microserver.tests.es_test',
    # 'microserver.tests.mongodb_test',
    # 'microserver.tests.mysql_test',
    # 'microserver.tests.redis_test'
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == "__main__":
    unittest.main(defaultTest="all")