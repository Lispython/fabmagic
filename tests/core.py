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
import os.path
from copy import deepcopy
from importlib import import_module
from types import ModuleType

import fabmagic
from fabmagic.core import configure_env, create_env
from fabmagic.utils import _throw_off_fabmagic

from .base import BaseTestCase

__all__ = 'CoreTestCase',


class CoreTestCase(BaseTestCase):
    """Test core utils of Fabric Magic Recipes
    """

    def test_configure_env(self):
        configured_env = configure_env(self.config_file)

        for key, value in self.configs_dict.iteritems():
            self.assertEquals(configured_env[key], value)

    def test_create_env(self):
        self.assertFalse(os.path.exists(self.new_config_file))
        create_env(self.new_config_file)
        self.assertTrue(os.path.exists(self.new_config_file))

    def test_configure_recipe(self):
        from fabric.state import env
        import fabmagic.redis
        d = {"some": "param"}
        configured_env = fabmagic._configure_recipe(fabmagic.redis, "redis", d)
        self.assertEquals(env.__module__, configured_env.__module__)
        d.update(fabmagic.redis.recipe_config)
        self.assertEquals(env[fabmagic.RECIPES_CONFIGS_KEY]["redis"], d)
        self.env = deepcopy(self.env_copy)

    def test_make_recipe_dict(self):
        item = "item value"

        recipe_dict = fabmagic._make_recipe_dict(item, "test.pa.th")
        self.assertEquals({'test': {'pa': {'th': item}}}, recipe_dict)

        recipe_dict = fabmagic._make_recipe_dict(item, "fabmagic.test.pa.th")
        self.assertEquals({'test': {'pa': {'th': item}}}, recipe_dict)

    def test_namespace_from(self):
        self.assertEquals(fabmagic._namespace_from(None), None)
        self.assertEquals(fabmagic._namespace_from("name.space"), "name.space")
        self.assertEquals(fabmagic._namespace_from(fabmagic.redis), fabmagic.redis.__name__)

    def test_get_recipe_config(self):
        import fabmagic.redis
        d = {"some1": "param1"}
        fabmagic._configure_recipe(fabmagic.redis, "redis", d)
        d.update(fabmagic.redis.recipe_config)
        self.assertEquals(d, get_recipe_config('redis'))

    def test_get_recipe_config_param(self):
        import fabmagic.redis
        d = {"some2": "param2"}
        fabmagic._configure_recipe(fabmagic.redis, "redis", d)
        d.update(fabmagic.redis.recipe_config)
        self.assertEquals(d["some2"], get_recipe_config_param("redis", "some2"))

    def test_get_recipe_roles(self):
        import fabmagic.redis
        d = {"roles": ["role1", "role2", "role3"]}
        fabmagic._configure_recipe(fabmagic.redis, "redis", d)
        d.update(fabmagic.redis.recipe_config)
        self.assertEquals(d["roles"], get_recipe_roles("redis"))

    def test_get_recipe_hosts(self):
        import fabmagic.redis
        d = {"hosts": ['host1', 'host2', 'host3']}
        fabmagic._configure_recipe(fabmagic.redis, "redis", d)
        d.update(fabmagic.redis.recipe_config)
        self.assertEquals(d["hosts"], get_recipe_hosts("redis"))

    def test_throw_off_fabmagic(self):
        self.assertEquals(_throw_off_fabmagic("fabmagic.some.path"), "some.path")
        self.assertEquals("some.path", "some.path")

    def test_recipe_template(self):
        self.assertEquals(get_recipe_template(), os.path.abspath(_rel(fabmagic.__path__[0], TEMPLATES_DIR_NAME, 'template')))


    def test_configure_recipes(self):
        from fabmagic import redis
        recipes = [("nginx", {"roles": ["web1", "web2"]}),
                   "monit",
                   "recipes",
                   "deploy",
                   "frameworks",
                   "frameworks.django",
                   redis]
        fabmagic.configure_recipes(*recipes)
        self.assertTrue(isinstance(fabmagic.env.magic_recipes, dict))

        for recipe in recipes:
            if isinstance(recipe, (tuple, list)):
                for key, value in recipe[1].iteritems():
                    self.assertEquals(fabmagic.env.magic_recipes[recipe[0]][key], value)
            else:
                if isinstance(recipe, ModuleType):
                    m = recipe
                    recipe = m.__name__
                else:
                    m = import_module("fabmagic.{0}".format(recipe))

                self.assertEquals(fabmagic.env.magic_recipes[_throw_off_fabmagic(recipe)],
                                  getattr(m, "recipe_config", fabmagic.utils.RecipeConfig()))
        self.env = deepcopy(self.env_copy)