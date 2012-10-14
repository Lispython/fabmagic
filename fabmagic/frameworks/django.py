#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fabmagic.frameworks.django
~~~~~~~~~~~~~~~~~~~~~~~~~~

Magic Fabric Recipes for django webframework

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric import colors
from fabric.utils import puts

from ..utils import RecipeConfig, magic_task

__all__ = 'create_settings', 'syncdb',

recipe_config = RecipeConfig({
    "roles": ["web"],
    })


@magic_task
def create_settings():
    """Create django config
    """
    puts(colors.blue("{0} create settings".format(__name__)))


@magic_task
def syncdb(migrate=False):
    """Sync database

    :param migrate: migration flag
    """
    puts(colors.blue("{0} syncdb".format(__name__)))


