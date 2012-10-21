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

module_config = ModuleConfig({
    "roles": ["key.db"]})

@magic_task
def start():
    """Start redis
    """
    puts(colors.blue("{0} successfull started".format(__name__)))


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
def status():
    """Redis status
    """
    puts(colors.blue("{0} status".format(__name__)))
