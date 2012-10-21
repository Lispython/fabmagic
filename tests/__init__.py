#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
fabmagic.tests
~~~~~~~~~~~~~~

tests

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

import unittest

from .cookbooks import CookbookTestCase, RolesTestCase
from .core import CoreTestCase


def suite():
    suite = unittest.TestSuite()
    ## suite.addTest(unittest.makeSuite(ReceptorTestCase))
    ## suite.addTest(unittest.makeSuite(BaseTestCase))
    suite.addTest(unittest.makeSuite(CookbookTestCase))
    ##suite.addTest(unittest.makeSuite(CoreTestCase))
    suite.addTest(unittest.makeSuite(RolesTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
