#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.manager
~~~~~~~~~~~~~

Manage recipes

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fabric.utils import puts, abort
from fabric.state import env
from fabric import colors

from .utils import _rel, ModuleConfig, magic_task


__all__ = "create_recipe",


recipe_config = ModuleConfig({
    "env_conf": _rel(os.path.curdir, ".config")})


@magic_task
def recipe_create(name):
    """Create recipe directory with name

    :param name: recipe name
    """
    #cd recipes /
    # mkdir recipes/name
    pass


@magic_task
def recipe_delete():
    pass
