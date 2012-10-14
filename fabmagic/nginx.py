#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fabmagic.nginx
~~~~~~~~~~~~~~

Magic Fabric Recipes to deploy nginx

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric.utils import puts
from fabric.api import run
from fabric import colors


from .utils import RecipeConfig, magic_task

__all__ = 'restart', 'stop', 'start', 'reload', 'status', 'recipe_config'


recipe_config = RecipeConfig({
    'conf': '/etc/nginx/sites-enabled/{project_name}.conf',
    'roles': ['web']})


@magic_task
def restart():
    """Restart nginx
    """

    puts(colors.blue("{0} successfull restarted".format(__name__)))


@magic_task
def stop():
    """Stop nginx service
    """
    puts(colors.blue("{0} successfull stoped".format(__name__)))


@magic_task
def start():
    """Start nginx service
    """
    puts(colors.blue("{0} successfull started".format(__name__)))


@magic_task
def reload():
    """Reload nginx configs
    """
    puts(colors.blue("{0} successfull reloaded".format(__name__)))


@magic_task
def status():
    """Nginx status
    """
    puts(colors.blue("{0} status".format(__name__)))
