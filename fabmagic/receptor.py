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
from .utils import _rel
from .constants import TEMPLATES_DIR_NAME


__all__ = '_rel', 'RecipeConfig', 'get_recipes_directory', 'get_recipe_path', 'get_recipe_template', \
          'get_recipe_info'


def get_recipes_directory():
    """Find recipes directory

    :return: path to recipes directory
    """
    if "recipes_path" in env.keys() and os.path.exists(env['recipes_path']):
        return env['recipes_path']
    elif os.path.exists(_rel(os.path.dirname(env.real_fabfile), 'recipes')):
        return _rel(os.path.dirname(env.real_fabfile), 'recipes')
    abort(colors.red("You need specify recipes_path"))


def get_recipe_path(name):
    """Get recipe path

    :param recipe: recipe name
    :return: recipe path
    :rtype: string, unicode
    """
    return _rel(get_recipes_directory(), name)


def get_recipe_def(name):
    """Get recipe definition

    :param recipe: recipe name
    :return: recipe path
    :rtype: string, unicode
    """
    recipe_path = get_recipe_path(name)
    def_path = os.path.join(recipe_path, "__init__.py")
    if not os.path.exists(def_path):
        abort(colors.red("Invalid recipe <{0}>: not found definition".format(name)))
    return def_path


def make_recipe_def_locals(name, recipe_def):
    """Make recipe definition locals dictionary

    :param name: recipe name
    :param recipe_def: recipe definition path
    :return: definition dictionary
    :rtype: dict
    """
    try:
        with open(os.path.join(os.path.dirname(recipe_def), "description")) as f:
            recipe_description = f.read()
    except Exception, e:
        puts(colors.red(e))
        recipe_description = None

    return {"__file__": recipe_def,
            "__name__": name,
            "__description__": recipe_description}


def get_recipe_info(name):
    """Get info from recipe

    :parma name: recipe name
    :return: dictionary of recipe parameters
    """
    recipe_def = get_recipe_def(name)

    recipe_locals = make_recipe_def_locals(name, recipe_def)
    # Provide node settings to locals
    execfile(recipe_def, {}, recipe_locals)

    # Return link to locals
    return recipe_locals


def execute_recipe(recipe):
    """Execute recipe file from ``recipe``

    :param recipe: execure recipe
    """
    puts("Execute recipe {0}".format(recipe))


def get_recipe_template(name='template'):
    """Get recipe template

    :param path: recipe template path
    """
    if "recipe_template" in env.keys() and os.path.exists(env['recipe_path']):
        return env['recipe_template']
    elif os.path.exists(_rel(fabmagic.__path__[0], TEMPLATES_DIR_NAME, name)):
        return _rel(fabmagic.__path__[0], TEMPLATES_DIR_NAME, name)

    abort(colors.red("You need specify recipes_path"))
