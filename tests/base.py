#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
fabmagic.tests.cookbooks
~~~~~~~~~~~~~~~~~~~~~~~~

Test cookbooks module

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

import os.path
import unittest
import logging
from copy import deepcopy
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


from fabric.state import env
from fabric.main import load_fabfile

from fabmagic.utils import _rel
from fabmagic.constants import COOKBOOKS_NAME, COOKBOOKS_LIBRARY_NAME, ROLES_NAME

__all__ = 'BaseTestCase',

logger = logging.getLogger("fabmagic.test")


env_copy = deepcopy(env)
current_dir = os.path.dirname(__file__)
fabfile_path = _rel(current_dir, "fabfile.py")
env.real_fabfile = fabfile_path
loading_result = load_fabfile(fabfile_path)

class BaseTestCase(unittest.TestCase):
    """Base test case
    """
    def setUp(self):
        self.logger = logger
        self.current_dir = current_dir
        self.fabfile_path = fabfile_path
        self.locading_result = loading_result
        self.env_copy = env_copy
        self.env = env
        self.config_file = _rel(os.path.dirname(__file__), ".config")
        self.new_config_file = _rel(os.path.dirname(__file__), ".new_config")

        config_file = open(self.config_file, 'r')
        config = load(config_file.read(), Loader=Loader)
        config_file.close()
        self.configs_dict = config
        self.env = env
        self.cookbooks_library_dir = self.rel(self.current_dir, COOKBOOKS_LIBRARY_NAME)
        self.cookbooks_roles_dir = self.rel(self.current_dir, COOKBOOKS_LIBRARY_NAME, ROLES_NAME)
        self.cookbooks_dir = self.rel(self.current_dir, COOKBOOKS_LIBRARY_NAME, COOKBOOKS_NAME)

    def tearDown(self):
        if os.path.exists(self.new_config_file):
            os.remove(self.new_config_file)

    @staticmethod
    def rel(*parts):
        return os.path.join(*parts)

