#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.fabfile
~~~~~~~~~~~~~~~~

Examples of Fabric Magic Recipes

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

import fabmagic


fabmagic.configure_recipes(
    "nginx",
    "monit",
    "deploy",
    "frameworks",
    "system")

