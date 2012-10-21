#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
memcahed recipe
~~~~~~~~~~~~~~~

Recipe to install and configure memcached

:copyright: (c) 2011 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

__author__ = "Alexandr Lispython"
__author_email__ = "alex@obout.ru"
__maintainer__ = "Alexandr Lispython"
__maintainer_email__ = "alex@obout.ru"
__license__ = "BSD"
__version_info__ = (0, 0, 1)
__version__ = ".".join(map(str, __version_info__))
__short_description__ = "Install and configure memcached"

# drafts
# recipe_dir = 'recipes'
# requirements = ['recipe_name_1', 'recipe_name_2']
# Setup nginx and postgres before memcahed
depends_on = 'postgres', 'nginx'

# Redefine __description__
# __description__ = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "description")).read()
