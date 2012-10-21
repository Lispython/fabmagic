#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fabmagic.monit
~~~~~~~~~~~~~~

Recipes to deploy nginx

:copyright: (c) 2011 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric import colors
from fabric.utils import puts

from .utils import ModuleConfig, magic_task

__all__ = 'fabmagic', 'restart', 'stop', 'start', 'create_config', 'module_config'

module_config = ModuleConfig({
    "roles": ['all']})

@magic_task
def start():
    """Start monit
    """
    puts(colors.blue("{0} successfull start".format(__name__)))


@magic_task
def stop():
    """Stop monit
    """
    puts(colors.blue("{0} successfull stoped".format(__name__)))


@magic_task
def restart():
    """Restart monit
    """
    puts(colors.blue("{0} successfull restarted".format(__name__)))


@magic_task
def create_config():
    """Create monit configs
    """
    puts(colors.blue("{0} create config".format(__name__)))
