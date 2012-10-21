#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.manager
~~~~~~~~~~~~~~~~

Manage cookbooks

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os

from shutil import copytree, ignore_patterns, rmtree

from fabric.api import task, run as remote_run
from fabric.state import env
from fabric.utils import puts, abort, indent
from fabric.context_managers import lcd
from fabric.contrib.console import confirm
from fabric import colors

from .constants import DEFAULT_INFO_SKIP_LIST
from .utils import magic_task
from .receptor.cookbooks import get_cookbooks_list, get_cookbook_dir, get_cookbook_info
from .receptor.utils import get_template, get_component_directory

__all__ = "create", "delete", "show", "info", "run"


def get_info_skip_list():
    """Get recipe params skip list

    :return: list of param names
    :rtype: list
    """
    if "info_skip_list" in env.keys() and isinstance(env['info_skip_list'], (tuple, list)):
        return env['info_skip_list']
    else:
        return DEFAULT_INFO_SKIP_LIST


@task
def create(name, location=False, force=False):
    """Create cookbook directory from template

    :param name: cookbook name
    """
    cookbook_path = get_cookbook_dir(name)
    with lcd(get_component_directory('cookbooks')):

        # Force overwrite
        if force:
            delete(name)

        if os.path.exists(cookbook_path):
            abort(colors.red("<{0}> cookbook already exists".format(name)))

        copytree(get_template(), cookbook_path, ignore=ignore_patterns('*.pyc', ' *.pyo'))
        puts(colors.green("Cookbook directory {0} created".format(name)))

        # Show location if needed
        if location:
            puts(colors.blue("Recipe {0} location: {1}".format(name, cookbook_path)))


@task
def delete(name, force=False):
    """Delete recipe directory with ``name``

    :param name: name
    """
    recipe_path = get_cookbook_dir(name)

    if force or confirm("Are you sure to delete <{0}> with path: {1}".format(name, recipe_path), default=force):
        rmtree(recipe_path)
        puts(colors.green("Cookbook <{0}> successfull removed from: {1}".format(name, recipe_path)))


@task
def info(cookbook):
    """Show cookbook info

    :param cookbook: cookbook name
    """
    recipe_path = get_cookbook_dir(cookbook)
    if not os.path.exists(recipe_path):
        abort(colors.red("Recipe <{0}> don't exists".format(cookbook)))

    cookbook_info = get_cookbook_info(cookbook)
    puts(colors.blue("Show <{0}> recipe params".format(cookbook)))

    for key, value in sorted(cookbook_info.iteritems(), key=lambda x: x[0]):
        if key not in get_info_skip_list():
            puts(colors.blue(indent("{0}: {1}".format(
                key.strip("__").replace("_", " "), value, indent=4))))
    puts("-" * 70)


@task
def show(cookbook=None, i=False, a=None, nested=False):
    """Show cookbooks
    """

    # Show details about specified recipe
    if cookbook and os.path.exists(get_cookbook_dir(cookbook)):
        if i:
            info(cookbook)
        else:
            puts(colors.blue("Recipe <{0}> on {1}".format(cookbook, get_cookbook_dir(cookbook))))
        return

    puts(colors.blue("Show all recipes <{0}>".format(get_component_directory('cookbooks'))))

    for cookbook in get_cookbooks_list():
        if i:
            info(cookbook)
        else:
            puts(colors.blue("Recipe <{0}> on {1}".format(cookbook, get_cookbook_dir(cookbook))))


@magic_task
def run(recipes=None):
    """Execute recipes on hosts
    """
    if recipes:
        recipes_list = recipes.split()
    else:
        try:
            recipes_list = env['recipes_list']
        except IndexError:
            recipes_list = get_recipes_list()
    puts(colors.blue("Execute [{0}] recipes".format(", ".join(recipes_list))))

    prepared_recipes = prepare_recipes_list(recipes_list)
    print(prepared_recipes)
