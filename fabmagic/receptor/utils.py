#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.receptor
~~~~~~~~~~~~~~~~~~~~~~~~

Fabric Magic Recipes module that provides recipes execution

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os.path


from fabric.api import abort, puts
from fabric.state import env
from fabric import colors

import fabmagic
from ..utils import _rel
from ..constants import TEMPLATES_DIR_NAME, COOKBOOKS_NAME, COOKBOOKS_LIBRARY_NAME


__all__ = 'get_component_directory', 'get_template', 'get_library_dir'


def get_library_dir():
    """Get global library path
    Library store roles and cookbooks
    """
    key = COOKBOOKS_LIBRARY_NAME
    if key in env.keys() and os.path.exists(env[key]):
        return env[key]
    return _rel(os.path.dirname(env.real_fabfile), COOKBOOKS_LIBRARY_NAME)


def get_component_directory(name):
    """Get directory for given component

    Components:
    - roles
    - cookbooks

    :param name: component name
    :return: path to component directory
    """
    key = '_'.join([name, 'path'])
    if key in env.keys():
        return env[key]
    return _rel(get_library_dir(), name)


def get_template(name='cookbook'):
    """Get recipe template

    :param path: recipe template path
    """
    if "cookbook_template" in env.keys() and os.path.exists(env['cookbook_path']):
        return env['cookbook_template']
    elif os.path.exists(_rel(fabmagic.__path__[0], TEMPLATES_DIR_NAME, name)):
        return _rel(fabmagic.__path__[0], TEMPLATES_DIR_NAME, name)
    abort(colors.red("You need specify recipes_path"))
