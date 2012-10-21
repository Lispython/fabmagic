#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.system
~~~~~~~~~~~~~~~

System utilities

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric.api import run, settings, hide

from .utils import ModuleConfig, magic_task

__all__ = 'hostname', 'uname', 'module_config'


module_config = ModuleConfig({
    "roles": ["all"]})


@magic_task
def uname(keys=None):
    """Show system uname output
    """
    with settings(hide('running')):
        cmd = "uname"
        if keys:
            cmd += " " + keys
        run(cmd)


@magic_task
def hostname():
    """Get host name
    """

    r = run('hostname --fqdn')
    return r
