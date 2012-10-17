











































































#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
default
~~~~~~~

Recipe example that use some DSL from contextmanagers


:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabmagic import env
from fabmagic.contextmanagers import Package, Directory, User



# Remove packages
for package in ['postgresql-client-9.1', 'postgresql-contrib-9.1', 'postgresql']:
    # delete packege
    with Package(package, **{"param": "some_param_value"}) as p:
        p.action = p.DELETE

# Create directory with mode 0755
with Directory(env['receptors']['directories']['log_dir']) as d:
    d.mode = 0755
    d.owner = d.env['nginx']
    d.action = Directory.CREATE


# Create user
with User("test_user") as u:
    d.home = '/home/test_user'
