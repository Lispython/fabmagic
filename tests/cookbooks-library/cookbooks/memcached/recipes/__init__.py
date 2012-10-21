#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Recipe Name
~~~~~~~~~~~

Recipe Description

You need change this decsription

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""
# no need imports, because it's passed into locals
machine = locals()['machine']
recipe_name = locals()['recipe_name']

with Package("memcached") as p:
    p.action = p.UPGRADE


with Package("libmemcache-dev") as p:
    if machine.platform in ['redhat', 'centos', 'fedora']:
        p.package_name = 'libmemcached-devel'
    else:
        p.package_name = 'libmemcached-dev'
    p.action = p.UPGRADE


with Service('memcahed') as s:
    s.action = s.NOTHING

# Machine params from roles or recipe attributes
if machine.platform in ['redhat', 'centos', 'fedora']:
    with Template('/etc/sysconfig/memcached') as t:
        # Add support different template engine
        t.source = 'memcached.sysconfig.template'
        t.owner = 'root'
        t.group = 'root'
        t.mode = 0644
        t.context = {
            "listen": machine[recipe_name]['listen'],
            "user": machine[recipe_name]['user'],
            "port": machine[recipe_name]['port'],
            "maxconn": machine[recipe_name]['maxconn'],
            "machine": machine[recipe_name]['memory']}
else:
    with Template('/etc/memcached.conf') as t:
        # Add support different template engine
        t.source = 'memcached.conf.template'
        t.owner = 'root'
        t.group = 'root'
        t.mode = 0644
        t.context = {
            "listen": machine[recipe_name]['listen'],
            "user": machine[recipe_name]['user'],
            "port": machine[recipe_name]['port'],
            "maxconn": machine[recipe_name]['maxconn'],
            "machine": machine[recipe_name]['memory']}
