#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.utils
~~~~~~~~~~~~~~

Core utilities, decorators

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

from .constants import RECIPES_CONFIGS_KEY

__all__ = 'get_templates_dir', '_rel', 'RecipeConfig', 'get_recipe_roles', \
          '_throw_off_fabmagic', 'magic_task', 'MagicTask'


def _rel(*parts):
    return os.path.join(*parts)


class RecipeConfig(_AttributeDict):
    """Recipe config
    """


def get_recipe_config(recipe):
    """Get recipe config from environment

    :param recipe: recipe name
    :type recipe: string
    """
    recipe_key = _throw_off_fabmagic(recipe)
    recipe_config = env[RECIPES_CONFIGS_KEY][recipe_key]
    return recipe_config


def get_recipe_config_param(recipe, param):
    """Recipe config parameter

    :param recipe: recipe name
    :type recipe: string
    :param param: config parametre to lookup
    :type param: string, list, tupe
    :return: parameter or None
    :rtype: value
    """
    try:
        recipe_config = get_recipe_config(recipe)
        if isinstance(param, (str, unicode)):
            return recipe_config[param]
        elif isinstance(param, (list, tuple)):
            item = recipe_config
            for key in param:
                item = item[key]
            return item
        abort("Invalid param [{0!r}] for get_recipe_config_param".format(param))
    except (KeyError, AttributeError):
        return None


def get_recipe_roles(recipe):
    """Get roles for `recipe`

    :param recipe: recipe to get roles
    :type recipe: string
    :return: list of roles
    :rtype: list
    """
    return get_recipe_config_param(recipe, "roles") or []


def get_recipe_hosts(recipe):
    """Get hosts for ``recipe``

    :param recipe: recipe to get roles
    :type recipe: string
    :return: list of roles
    :rtype: list
    """
    return get_recipe_config_param(recipe, "hosts") or []


def _throw_off_fabmagic(namespace):
    """Get recipe name from f

    :param namespace: namespace string
    :type namespace: string, unicode
    """
    splited = namespace.split(".")
    if splited[0] == 'fabmagic':
        splited.remove('fabmagic')
    return '.'.join(splited)


class MagicTask(WrappedCallableTask):
    """Replace standard :class:`~fabric.
    """

    def get_hosts(self, arg_hosts, arg_roles, arg_exclude_hosts, env=None):
        """Get hosts by priority

        :param arg_hosts: user command line specifed hosts
        :type arg_hosts: list
        :param arg_roles: user commend line specifed roles
        :type arg_roles: list
        :param arg_exclude_hosts: user command line specifed hosts to exclude
        :type arg_exclude_hosts: list
        :param env: :class:`~fabric.utils._AttributeDict` object with env
        :type env: `~fabric.utils._AttributeDict`
        """
        env = env or {'hosts': [], 'roles': [], 'exclude_hosts': []}
        roledefs = env.get('roledefs', {})
        # Command line per-task takes precedence over anything else.
        if arg_hosts or arg_roles:
            return merge(arg_hosts, arg_roles, arg_exclude_hosts, roledefs)

        # Use recipe configured roles
        recipe_roles = get_recipe_roles(self.wrapped.__module__)
        recipe_hosts = get_recipe_hosts(self.wrapped.__module__)

        if recipe_roles or recipe_hosts:
            return merge(recipe_hosts, recipe_roles, arg_exclude_hosts, roledefs)

        # Decorator-specific hosts/roles go next
        func_hosts = getattr(self, 'hosts', [])
        func_roles = getattr(self, 'roles', [])
        if func_hosts or func_roles:
            return merge(func_hosts, func_roles, arg_exclude_hosts, roledefs)
        # Finally, the env is checked (which might contain globally set lists
        # from the CLI or from module-level code). This will be the empty list
        # if these have not been set -- which is fine, this method should
        # return an empty list if no hosts have been set anywhere.
        env_vars = map(_get_list(env), "hosts roles exclude_hosts".split())
        env_vars.append(roledefs)
        return merge(*env_vars)


def magic_task(*args, **kwargs):
    """
    Decorator declaring the wrapped function to be a new-style task.

    Copy-paste from original ``fabric.decorators`` but replaces task_class
    Need to use roles from configured recipes

    """
    invoked = bool(not args or kwargs)
    task_class = kwargs.pop("task_class", MagicTask)
    if not invoked:
        func, args = args[0], ()

    def wrapper(func):
        # TODO: attach magic recipe config link to wrapped object
        return task_class(func, *args, **kwargs)

    return wrapper if invoked else wrapper(func)
