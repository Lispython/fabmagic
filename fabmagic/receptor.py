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

from fabric.api import abort
from fabric.utils import  _AttributeDict
from fabric.state import env
from fabric.task_utils import merge
from fabric.tasks import WrappedCallableTask, _get_list

from .utils import RecipeConfig

__all__ = '_rel', 'RecipeConfig', 'get_recipes_directory'


recipe_config = RecipeConfig()


def get_recipes_directory():
    """Find recipes direcotory
    """
    pass


def execute_recipe(recipe_path):
    """Execute recipe file from ``recipe_path``
    """
    pass

