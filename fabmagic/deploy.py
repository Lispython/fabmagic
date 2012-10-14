#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.deploy
~~~~~~~~~~~~~~~

Tasks to deploy

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""


from fabric.utils import puts
from fabric import colors

from .utils import magic_task, RecipeConfig

__all__ = 'releases', 'cleanup', 'rollback'

recipe_config = RecipeConfig()


@magic_task
def releases():
    """Show deployes releases
    """
    puts(colors.green("Tring to show releases"))
    ## with cd(env.releases):
    ##     releases = run("ls")
    ##     current_release = run("cat {0}".format(_rel(env.current, "RELEASED")))
    ##     puts("Current release {0}".format(current_release))

    ##     for x in sorted(releases.split(), reverse=True):
    ##         if current_release == x:
    ##             puts(colors.green("{0}<--------- current".format(_rel(env.releases,  x.strip()))))
    ##         else:
    ##             puts(colors.green("{0}".format(_rel(env.releases,  x.strip()))))


@magic_task
def cleanup(num=5):
    """Clean up old releases.
    """
    puts(colors.green("Tring to cleanup"))
    ## if num <= 1:
    ##     abort("You can't cleanup all releases")

    ## with cd(env.releases):
    ##     releases = run("ls")
    ##     for x in sorted(releases.split(), reverse=True)[num:]:
    ##         if x != "current" or x != "previuos":
    ##             run("rm -rf %s" % _rel(env.releases,  x.strip()))


@magic_task
def rollback(release=None):
    """Rollback previous successes release as current

    :param release: release time stamp
    :param llist: show old releases
    """
    puts(colors.green("Tring to rollback"))
