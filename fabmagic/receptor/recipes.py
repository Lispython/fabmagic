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
from ..constants import TEMPLATES_DIR_NAME, COOKBOOKS_NAME
from .utils import get_component_directory

__all__ = '_rel', 'get_recipes_directory', 'get_recipe_path', 'get_template', \
          'get_recipe_info', 'execute_recipe'


def get_recipes_list(cook):
    """Get recipes list by given
    :return: list of recipes names
    """
    return os.listdir(get_recipes_directory())

def prepare_recipes_list(recipes):
    """Prepare recipes list
    Sort recipes by requirements

    :param recipes: list of recipe names
    :return: recipes prepared data
    """
    res = []
    for recipe in recipes:
        res.append((recipe, get_recipe_info(recipe)))

    return res


def prepare_recipe(name):
    """Validate recipe before execution

    :param name: prepare recipe name
    """
    return get_recipe_info(name)


def get_recipes_directory():
    """Find recipes directory

    :return: path to recipes directory
    """
    return get_component_directory('recipes')


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
