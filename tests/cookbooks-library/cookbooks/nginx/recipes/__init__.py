#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Recipe Name
~~~~~~~~~~~

Recipe Description

You need change this decsription

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

with Package('nginx') as p:
    p.action = p.INSTALL


with Directory(machine['log_dir']) as p:
    p.mode = 0755
    p.owner = machine['user']
    p.action = p.CREATE

for i in ['nxensite', 'nxdissite']:
    with Template('/usr/bin/{0}'.format(i)) as t:
        t.source = '{0}.tmpl'.format(i)
        t.mode = 0755
        t.owner = 'root'
        t.group = 'root'

with Template('nginx.conf') as t:
    t.path = t.rel(machine['dir'], 'nginx.conf')
    t.source = 'nginx.conf.tmpl'
    t.owner = 'root'
    t.group = 'root'
    t.mode = 0644

with Template(Template.rel(machine['dir'], 'sites-available', 'default')) as t:
    t.source = 'default-site.tmpl'
    t.owner = 'root'
    t.group = 'root'
    t.mode = 0644

with Service('nginx') as s:
    s.supports = {"status": True,
                  "restart": True,
                  "reload": True}
    s.action = s.START
