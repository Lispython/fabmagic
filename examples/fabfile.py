#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.examples.fabfile
~~~~~~~~~~~~~~~~~~~~~~~~~

Examples of Fabric Magic Recipes

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

import fabmagic
import fabmagic.redis

from fabric.state import env

fabmagic.configure_recipes(
    ("nginx", {"test_key": "test_value"}),
    "monit",
    "redis",
    "deploy",
    "frameworks.django",
    # Reset preconfigured recipe_config.roles
    ("system", {"roles": ["system", "db"]})
    )

machine1 = {"host": "vagrant@33.33.33.10",
            "password": "vagrant"}

machine2 = {"host": "vagrant@33.33.33.11",
            "password": "vagrant"}


@fabmagic.magic_task
def production():
    """Reconfigure to production
    """

    env.roledefs.update({
        'web': [machine1['host'], machine2['host']],
        'db': [machine1['host']],
        'system': [machine2['host']]},)

    env.passwords = {
        machine1['host']: machine1['password'],
        machine2['host']: machine2['password']}


@fabmagic.magic_task
def stage():
    """Reconfigure to stage
    """
    production()


@fabmagic.magic_task
def show_env():
    """Show environment
    """
    from pprint import pprint
    pprint(env)
