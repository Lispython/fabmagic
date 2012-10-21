#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
fabmagic.tests.cookbooks
~~~~~~~~~~~~~~~~~~~~~~~~

Test cookbooks module

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""
import os
import unittest

from fabmagic.receptor.roles import get_roles_dir, get_role_info,\
     get_roles_list, get_role_path
from fabmagic.receptor.utils import get_component_directory, get_library_dir
from fabmagic.receptor.recipes import get_recipes_list, prepare_recipes_list, prepare_recipe, \
     get_recipes_directory, get_recipe_path, get_recipe_def, make_recipe_def_locals, get_recipe_info, \
     execute_recipe

from fabmagic.receptor.cookbooks import get_cookbook_dir, get_cookbook_recipes, get_cookbook_recipe, \
     get_cookbook_attributes, make_cookbook_def_locals, get_cookbook_info

from fabmagic.constants import ATTRIBUTES_PATH_NAME

from .base import BaseTestCase

__all__ = 'CookbookTestCase', 'ReceptorTestCase', 'RolesTestCase',



class RolesTestCase(BaseTestCase):

    def test_roles_list(self):
        roles = map(lambda x: x.split('.')[0],
                    os.listdir(self.cookbooks_roles_dir))
        roles_list = get_roles_list()

        for role in roles:
            self.assertTrue(role in roles_list)

    def test_roles_path(self):
        self.assertEquals(get_roles_dir(), self.cookbooks_roles_dir)
        self.assertEquals(get_role_path('web'), self.rel(self.cookbooks_roles_dir, 'web.py'))

    def test_role_info(self):
        role = 'web'
        role_info = get_role_info(role)
        self.assertEquals(role_info['name'], "web-role-name")
        self.assertEquals(role_info['description'], "Role description")
        self.assertEquals(role_info['run_list'], ('recipe.nginx', 'recipe.postgres.recipename'))
        self.assertEquals(role_info['depends_on'], ('sudo', 'sysctl'))


class CookbookTestCase(BaseTestCase):
    """Test cookbook functions
    """
    def test_cookbook_dir(self):
        self.assertEquals(self.cookbooks_dir, get_component_directory('cookbooks'))

        self.assertEquals(self.rel(self.cookbooks_dir, 'nginx'),
                          get_cookbook_dir('nginx'))

    def test_cookbook_recipes(self):
        cookbooks = map(lambda x: x.split('.')[0],
                    filter(lambda x: x.endswith(".py"),
                           os.listdir(self.rel(self.cookbooks_dir, 'memcached', 'recipes'))))

        cookbooks_list = get_cookbook_recipes('memcached')
        self.assertEquals(len(cookbooks_list), 2)
        for cookbook in cookbooks:
            self.assertTrue(cookbook in cookbooks_list)

        self.assertEquals(get_cookbook_recipe('memcached'),
                          self.rel(get_cookbook_dir('memcached'), 'recipes', '__init__.py'))
        self.assertEquals(get_cookbook_recipe('memcached', 'main'),
                          self.rel(get_cookbook_dir('memcached'), 'recipes', 'main.py'))

    def test_cookbook_attributes(self):

        cookbook_attributes = get_cookbook_attributes('memcached')
        self.assertEquals(cookbook_attributes['memory'], 64)
        self.assertEquals(cookbook_attributes['port'], 11211)
        self.assertEquals(cookbook_attributes['user'], 'nobody')
        self.assertEquals(cookbook_attributes['listen'], '0.0.0.0')
        self.assertEquals(cookbook_attributes['maxconn'], 1024)

        # TODO: chech attributes in node env

        cookbook_attributes_nginx = get_cookbook_attributes('nginx')
        self.assertEquals(cookbook_attributes_nginx['some_var'], "some value")
        self.assertEquals(cookbook_attributes_nginx['another_var'], "another value")
        for attr_file in map(lambda i: i.split(".")[0],
                             filter(lambda x: x.endswith(".py"),
                                    os.listdir(self.rel(self.cookbooks_dir, 'nginx',
                                                        ATTRIBUTES_PATH_NAME)))):
            if attr_file == '__init__': continue
            self.assertTrue(attr_file in cookbook_attributes_nginx.keys())


    def test_cookbook_info(self):
        cookbook_info = get_cookbook_info("nginx")
        self.assertEquals(cookbook_info['__author__'], "Alexandr Lispython")
        self.assertEquals(cookbook_info['__author_email__'], 'alex@obout.ru')
        self.assertEquals(cookbook_info['__maintainer__'], 'Alexandr Lispython')
        self.assertEquals(cookbook_info['__license__'], 'BSD')
        self.assertEquals(cookbook_info['__version_info__'], (0, 0, 7))
        self.assertEquals(cookbook_info['__version__'], '0.0.7')
        self.assertEquals(cookbook_info['__short_description__'],
                          'test short nginx recipe description')

    def test_cookbook_def(self):
        cookbook_name = 'nginx'
        self.assertEquals(make_cookbook_def_locals(cookbook_name),
                          {"__file__": self.rel(self.cookbooks_dir, cookbook_name, "__init__.py"),
                           "__path__": self.rel(self.cookbooks_dir, cookbook_name),
                           "__name__": cookbook_name,
                           "__description__": open(self.rel(get_cookbook_dir(cookbook_name), "description")).read()})
