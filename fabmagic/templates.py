#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.templates
~~~~~~~~~~~~~~~~~~

Utilities to manage templates

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
import os.path
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fabric.utils import puts, abort
from fabric.state import env
from fabric import colors

from . import __path__ as fabmagic_path
from .utils import _rel, RecipeConfig
from .constants import TEMPLATES_DIR_NAME

__all__ = 'recipe_config', 'get_template_path'


recipe_config = RecipeConfig({
    "env_conf": _rel(os.path.curdir, ".config")})


def get_template_path(name):
    """Get templates from local templates dirs or fabmagic
    templates directory
    """
    if isinstance(name, (str, unicode)):
        name_list = [name]

    if 'templates_path' in env and os.path.exists(env['templates_path']) and\
           os.path.exists(_rel(env['templates_path'], *name_list)):
        return _rel(env['templates_path'], *name_list)

    template_path = _rel(os.path.dirname(env.real_fabfile), TEMPLATES_DIR_NAME, *name_list)
    if os.path.exists(template_path):
        return template_path

    template_path = _rel(fabmagic_path[0], TEMPLATES_DIR_NAME, *name_list)
    if os.path.exists(template_path):
        return template_path

    return None
