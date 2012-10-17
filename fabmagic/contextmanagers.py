#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fabmagic.contextmanagers
~~~~~~~~~~~~~~~~~~~~~~~~

Fabric Magic Recipes context managers


:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/fabmagic
"""

from fabric.state import env


__all__ = 'BaseContextManager', 'Package', 'User', 'Directory'

# SIGNATURES

CREATE = 0x000001
DELETE = 0x000002
MOVE = 0x000003


class BaseContextManager(object):
    """Base class for Fabmagic Context managers
    """

    def run(self):
        """Run context manager processing
        """
        raise NotImplementedError("Context processor run not specified")

    def __enter__(self):
        """Enter to contextmanager namespace

        :return: :class:`PackageInstall` object
        """
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        """Exit from contextmanager namespace
        """
        self.run()



class Package(BaseContextManager):
    """Context packages installer
    """
    def __init__(self, package_name):
        self._package_name = package_name

    def run(self):
        """Run context namage processing
        """
        print("Execute command on machine1")


class Directory(BaseContextManager):
    """Context directory manager
    """
    CREATE = CREATE
    DELETE = DELETE
    MOVE = MOVE

    def __init__(self, username):
        self._username = username

    def run(self):
        """Run context manager processing
        """
        print("Execute directory creation on machine")
