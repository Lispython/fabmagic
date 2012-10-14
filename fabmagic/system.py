#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.system
~~~~~~~~~~~~~~~

System utilities

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric.api import run

from .utils import RecipeConfig, magic_task


__all__ = 'uname', 'recipe_config'


recipe_config = RecipeConfig({
    "roles": ["all"]})


@magic_task
def uname(keys=None):
    """Show system uname output
    """
    cmd = "uname"
    if keys:
        cmd += " " + keys
    run(cmd)
