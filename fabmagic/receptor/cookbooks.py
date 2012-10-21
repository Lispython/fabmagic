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
from ..constants import TEMPLATES_DIR_NAME, COOKBOOKS_NAME, ATTRIBUTES_PATH_NAME

from .utils import get_component_directory


__all__ = 'get_cookbooks_list', 'get_cookbook_dir', 'get_cookbook_recipes', \
          'get_cookbook_recipe', 'get_cookbook_attributes', 'make_cookbook_def_locals', \
          'get_cookbook_info'


def get_cookbooks_list():
    """Get cookbooks list

    :return: cookbooks list
    """
    return os.listdir(get_component_directory('cookbooks'))


def get_cookbook_dir(cookbook):
    """Get directory for single cookbook

    :param cookbook: cookbook name
    :return: path to cookbook
    :rtype: string
    """
    return _rel(get_component_directory('cookbooks'), cookbook)


def get_cookbook_recipes(cookbook):
    """Get recipes from single cookbook

    :param cookbook: cookbook name
    :return: path to cookbook
    :rtype: string
    """
    return map(lambda x: x.split(".")[0],
               filter(lambda x: x.endswith(".py"), os.listdir(_rel(get_cookbook_dir(cookbook), 'recipes'))))


def get_cookbook_recipe(cookbook, recipe="__init__"):
    """Get single recipe from single cookbook

    :param recipe: recipe in cookbook (default __init__.py)
    :param cookbook: cookbook name
    :return: path to recipe
    :trype: string
    """
    recipe = '.'.join([recipe, 'py']) if not recipe.endswith('.py') else recipe
    return _rel(get_cookbook_dir(cookbook), 'recipes', recipe)


def get_machine_info(host):
    """Get all info about host
    """
    return {"platform": "ubuntu",
            "cpu": {
                "total": "none"}}


def get_cookbook_attributes(name):
    """Get recipe attributes path

    :param name: recipe attributes path
    :rtype: string
    """
    cookbook_dir = get_cookbook_dir(name)
    attributes_locals = {'system': get_machine_info('test')}
    if os.path.isdir(_rel(cookbook_dir, ATTRIBUTES_PATH_NAME)):
        # collect attributes from files
        for attr_file, namespace, in map(lambda i: (i, i.split('.')[0]),
                                         filter(lambda x: x.endswith(".py"),
                                                os.listdir(_rel(cookbook_dir, ATTRIBUTES_PATH_NAME)))):
            if namespace == '__init__':
                execfile(_rel(cookbook_dir, ATTRIBUTES_PATH_NAME, attr_file), {},
                         attributes_locals)
            else:
                attributes_locals[namespace] = {'system': attributes_locals['system']}
                execfile(_rel(cookbook_dir, ATTRIBUTES_PATH_NAME, attr_file), {},
                         attributes_locals[namespace])
    else:
        # collect attribute from attributes/__init__.py
        execfile(_rel(cookbook_dir, ATTRIBUTES_PATH_NAME), {}, attributes_locals)
    return attributes_locals


def make_cookbook_def_locals(name):
    """Make recipe definition locals dictionary

    :param name: recipe name
    :param recipe_def: recipe definition path
    :return: definition dictionary
    :rtype: dict
    """
    cookbook_dir = get_cookbook_dir(name)
    try:
        with open(_rel(cookbook_dir, "description")) as f:
            recipe_description = f.read()
    except Exception, e:
        puts(colors.red(e))
        recipe_description = None

    return {"__file__": _rel(cookbook_dir, "__init__.py"),
            "__path__": cookbook_dir,
            "__name__": name,
            "__description__": recipe_description}

def get_cookbook_info(name):
    """Get info for given cookboon name

    :param name: cookbook name
    :return: dictionary in cookbook parameters
    """
    cookbook_locals = make_cookbook_def_locals(name)
    # Provide node settings to locals
    execfile(cookbook_locals['__file__'], {}, cookbook_locals)

    # Return link to locals
    return cookbook_locals
