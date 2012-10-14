#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.core
~~~~~~~~~~~~~

Core utilities

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fabric.utils import puts, abort
from fabric.state import env
from fabric import colors

from .utils import _rel, RecipeConfig


__all__ = 'configure_recipes', 'show_recipes', 'configure_env', \
          'create_env', 'recipe_config'


recipe_config = RecipeConfig({
    "env_conf": _rel(os.path.curdir, ".config")})


def show_recipes(nested=False):
    """Show available recipes

    :param nested: nested flag
    :type nested: boolean
    """
    puts(colors.blue("Show Fabric Magic Recipes"))


def configure_env(env_file=recipe_config.env_conf):
    """Configure environment from YAML file

    :param env_file: path to config file
    :type env_file: string
    :return: :class:`fabric.state.env` object
    :rtype: :class:`fabric.state.env`
    """
    puts("Use {0} for configure environment".format(env_file))
    if not os.path.exists(env_file):
        abort("Deploy configuration file doesn't exists")

    config_file = open(env_file, 'r')
    config = load(config_file.read(), Loader=Loader)
    config_file.close()
    env.update(config)
    return env


def create_env(config=recipe_config.env_conf):
    """Create default environment file

    :param config: config path string
    :type config: string
    """
    data_structure = {}
    i = 1
    while os.path.exists(config):
        config = config + str(i)
        i += 1

    config_file = file(config, 'w')
    dump(data_structure, config_file, Dumper=Dumper)
    puts("{0} successfull created".format(__name__))
