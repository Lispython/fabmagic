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
from shutil import copytree, ignore_patterns, rmtree

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fabric.api import task
from fabric.state import env
from fabric.utils import puts, abort, indent
from fabric.context_managers import lcd
from fabric.contrib.console import confirm
from fabric import colors

from .constants import DEFAULT_INFO_SKIP_LIST
from .utils import magic_task
from .receptor import get_recipes_directory, get_recipe_path, get_recipe_template, get_recipe_info

__all__ = "create", "delete", "show", "info"


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
    """Create recipe directory with name from

    :param name: recipe name
    """
    recipe_path = get_recipe_path(name)
    with lcd(get_recipes_directory()):

        # Force overwrite
        if force:
            delete(name)

        if os.path.exists(recipe_path):
            abort(colors.red("<{0}> recipe already exists".format(name)))

        copytree(get_recipe_template(), recipe_path, ignore=ignore_patterns('*.pyc', ' *.pyo'))
        puts(colors.green("Recipes directory {0} created".format(name)))

        # Show location if needed
        if location:
            puts(colors.blue("Recipe {0} location: {1}".format(name, recipe_path)))


@task
def delete(name, force=False):
    """Delete recipe directory with ``name``

    :param name: name
    """
    recipe_path = get_recipe_path(name)

    if force or confirm("Are you sure to delete <{0}> with path: {1}".format(name, recipe_path), default=force):
        rmtree(recipe_path)
        puts(colors.green("Recipe <{0}> successfull removed from: {1}".format(name, recipe_path)))


@task
def info(recipe):
    """Show recipe info

    :param recipe:

    """
    recipe_path = get_recipe_path(recipe)
    if not os.path.exists(recipe_path):
        abort(colors.red("Recipe <{0}> don't exists".format(recipe)))

    recipe_info = get_recipe_info(recipe)
    puts(colors.blue("Show <{0}> recipe params".format(recipe)))

    for key, value in sorted(recipe_info.iteritems(), key=lambda x: x[0]):
        if key not in get_info_skip_list():
            puts(colors.blue(indent("{0}: {1}".format(
                key.strip("__").replace("_", " "), value, indent=4))))
    puts("-" * 70)


@task
def show(recipe=None, i=False, a=None, nested=False):
    """Show recipes

    """
    recipes_path = get_recipes_directory()

    # Show details about specified recipe
    if recipe and os.path.exists(get_recipe_path(recipe)):
        if i:
            info(recipe)
        else:
            puts(colors.blue("Recipe <{0}> on {1}".format(recipe, get_recipe_path(recipe))))
        return

    puts(colors.blue("Show all recipes <{0}>".format(recipes_path)))

    for d in os.listdir(recipes_path):
        info(d)
