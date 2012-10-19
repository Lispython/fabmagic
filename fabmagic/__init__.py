#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Collection of recipes for fabric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Magic Recipes for Fabric


:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

__all__ = 'VERSION', 'VERSION_INFO',\
          'create_env', 'configure_env',\
          'configure_recipes',\
          'env', 'magic_task', 'MagicTask',\
          'get_template_path'


__author__ = "Alex Lispython (alex@obout.ru)"
__license__ = "BSD, see LICENSE for more details"
__version_info__ = (0, 0, 1)
__build__ = 0x000001
__version__ = ".".join(map(str, __version_info__))
__maintainer__ = "Alexandr Lispython (alex@obout.ru)"

VERSION = __version__
VERSION_INFO = __version_info__

from importlib import import_module
from types import ModuleType

from fabric.utils import puts, abort
from fabric.state import env, commands
from fabric.main import load_tasks_from_module
from fabric import colors

from .core import configure_env, create_env
from .utils import RecipeConfig, _throw_off_fabmagic, magic_task, MagicTask
from .constants import RECIPES_CONFIGS_KEY, RECIPE_CONFIG_NAME, NAME_LIB, DEFAULT_INFO_SKIP_LIST
from .templates import get_template_path

assert configure_env
assert create_env
assert magic_task
assert MagicTask
assert get_template_path


if RECIPES_CONFIGS_KEY not in env:
    env[RECIPES_CONFIGS_KEY] = {}


def _configure_recipe(m, name, config_params):
    """Configure recipe module

    :param m: recipe module
    :type m: module
    :param name: recipe name
    :type name: string
    :param config_params: recipe custom params
    :type config_params: dict
    """
    config = getattr(m, RECIPE_CONFIG_NAME, RecipeConfig())
    config.update(config_params)
    splited_name = _throw_off_fabmagic(name).split(".")
    env[RECIPES_CONFIGS_KEY]['.'.join(splited_name)] = config
    return env


def _make_recipe_dict(item, namespace=None):
    """Convert namespace string to dict

    :param tasks: tasks dictionaty
    :type tasks: dict
    :param namespace: recipe namespace
    :type namespace: string
    :return: namespace as dict
    :rtype: dict
    """
    if not namespace:
        return item

    splited = _throw_off_fabmagic(namespace).split(".")
    res = item
    for part in reversed(splited):
        res = {part: res}
    return res


def _namespace_from(namespace):
    """Get string namespace from namespace

    :param namespace: namespace for
    :return: cleaned namespace name
    :rtype: string
    """
    if not namespace:
        return namespace
    elif isinstance(namespace, (str, unicode)):
        return namespace
    elif isinstance(namespace, ModuleType):
        return namespace.__name__


def _configure_module(name, namespace=None, config_params={}):
    """Configure module with namespace

    :param name: recipes file
    :type name: string
    :param namespace: namespace to module
    :type namespace: string
    :param config_params: custom recipe params
    :type config_params: dict
    """
    try:
        if isinstance(name, ModuleType):
            m = name
            name = m.__name__
        else:
            m = import_module("{0}.{1}".format(NAME_LIB, name))
    except Exception, e:
        abort("Can't import recipe {0}: {1}".format(name, e))
    docstring, new_style, classic, default = load_tasks_from_module(m)

    tasks = new_style if env.new_style_tasks else classic

    _configure_recipe(m, _namespace_from(m), config_params)
    commands.update(_make_recipe_dict(tasks, _namespace_from(namespace)))
    puts("{0} recipe configured".format(name))
    return True


def _recipe_repr(recipe):
    """Configure recipe

    :param recipe: recipe item (list, string)
    :type param: string, tuple, list
    """
    if isinstance(recipe, (str, unicode)):
        return recipe
    elif isinstance(recipe, ModuleType):
        return recipe.__name__
    elif isinstance(recipe, (tuple, list)):
        if isinstance(recipe[0], ModuleType):
            return recipe[0].__name__
        elif isinstance(recipe[0], (str, unicode)):
            return recipe[0]
        else:
            abort('Invalid recipe "{0!r}" to configurate'.format(recipe))
    else:
        abort('Invalid recipe "{0!r}" to configurate'.format(recipe))


def configure_recipes(*recipes):
    """Configure Magic Recipes and import it's to fabfile namespace

    :param \*recipes: list of available modules, without fabmagic prefix
    """
    puts(colors.red(
        "Configuring recipes: {0}".\
        format(", ".join(map(lambda x: _recipe_repr(x), recipes)))))
    recipes = list(recipes)

    _configure_module("core")

    for recipe in recipes:
        if isinstance(recipe, (tuple, list)) and len(recipe) > 1 and \
           isinstance(recipe[1], dict):
            _configure_module(recipe[0], recipe[0], recipe[1])
        elif isinstance(recipe, (str, unicode)):
            _configure_module(recipe, recipe)
        elif isinstance(recipe, ModuleType):
            _configure_module(recipe, recipe.__name__)
    env['info_skip_list'] = DEFAULT_INFO_SKIP_LIST
    puts(colors.blue("Recipes successfull configured"))
