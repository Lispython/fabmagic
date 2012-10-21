#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.receptor.roles
~~~~~~~~~~~~~~~~~~~~~~~

Helper to manipulate cookbook roles

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
import os.path

from ..utils import _rel
from .utils import get_component_directory


__all__ = 'get_roles_dir', 'get_foles_list', 'get_role_info', 'get_role_path'


def get_roles_dir():
    """Find roles directory

    :return: path to roles directory
    """
    return get_component_directory('roles')


def get_roles_list():
    """Get roles list by given

    :return: list of roles name
    """
    return map(lambda x: x.strip(".py"), os.listdir(get_roles_dir()))


def get_role_info(name):
    """Get info for role

    :param name: role name
    :return: dictionary of role params
    """
    role_path = get_role_path(name)
    role_locals = {}

    # Provide role settings to locals
    execfile(role_path, {}, role_locals)

    # Link to role locals
    return role_locals


def get_role_path(name):
    """Get path to role file

    :param name: role name
    :return: role file path
    :rtype: string, unicode
    """
    return _rel(get_roles_dir(), '.'.join([name, "py"]))
