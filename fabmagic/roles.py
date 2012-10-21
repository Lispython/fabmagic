#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.roles
~~~~~~~~~~~~~~

Manage roles

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
from shutil import copytree, ignore_patterns, copyfile

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fabric.api import task, run as remote_run
from fabric.state import env
from fabric.utils import puts, abort, indent
from fabric.context_managers import lcd
from fabric.operations import require
from fabric.contrib.console import confirm
from fabric import colors

from .utils import magic_task
from .receptor.roles import get_roles_dir, get_roles_list, get_role_info, get_role_path
from .receptor.utils import get_template

__all__ = "create", "delete", "show", "info"



@task
def create(name, location=False, force=False):
    """Create role

    :param name: role name
    """
    role_path = get_role_path(name)
    roles_path = get_roles_dir()

    if not os.path.exists(roles_path):
        puts(colors.green("Roles directory doesn't exist, creating"))
        os.mkdir(roles_path)

    with lcd(roles_path):

        # Force overwrite
        if force:
            delete(name)

        if os.path.exists(role_path):
            abort(colors.red("<{0}> recipe already exists".format(name)))

        copyfile(get_template('role.py'), role_path)
        puts(colors.green("Recipes directory {0} created".format(name)))

        # Show location if needed
        if location:
            puts(colors.blue("Recipe {0} location: {1}".format(name, role_path)))


@task
def delete(name=None, force=False):
    """Delete recipe directory with ``name``

    :param name: name
    """
    if not name:
        abort(colors.red("You need specify role name to delete"))

    role_path = get_role_path(name)

    if force or confirm("Are you sure to delete <{0}> with path: {1}".format(name, role_path), default=force):
        os.remove(role_path)
        puts(colors.green("Recipe <{0}> successfull removed from: {1}".format(name, role_path)))


@task
def info(role=None):
    """Show recipe info

    :param role:

    """
    if not role:
        abort(colors.red("You need specify role name"))
    role_path = get_role_path(role)
    if not os.path.exists(role_path):
        abort(colors.red("Role <{0}> don't exists".format(role)))

    role_info = get_role_info(role)
    puts(colors.blue("Show <{0}> role params".format(role)))

    for key, value in sorted(role_info.iteritems(), key=lambda x: x[0]):
        puts(colors.blue(indent("{0}: {1}".format(
            key.strip("__").replace("_", " "), value, indent=4))))
    puts("-" * 70)


@task
def show(role=None, i=True, a=None, nested=False):
    """Show recipes

    :param role: show single role
    :param i: ifo flag
    """
    roles_path = get_roles_dir()

    # Show details about specified recipe
    if role and os.path.exists(get_role_path(role)):
        if i:
            info(role)
        else:
            puts(colors.blue("Role <{0}> on {1}".format(role, get_role_path(role))))
        return

    puts(colors.blue("Show all roles <{0}>".format(roles_path)))

    for role in get_roles_list():
        if i:
            info(role)
        else:
            puts(colors.blue("Role <{0}> on {1}".format(role, get_role_path(role))))

