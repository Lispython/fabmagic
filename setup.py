#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Python fabric recipes
~~~~~~~~~~~~~~~~~~~~~

Collection of Magic recipes for fabric

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""

import os
import sys

from setuptools import setup

try:
    readme_content = open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "README.rst")).read()
except Exception, e:
    print(e)
    readme_content = __doc__

VERSION = "0.0.1"

py_ver = sys.version_info

#: Python 2.x?
is_py2 = (py_ver[0] == 2)

#: Python 3.x?
is_py3 = (py_ver[0] == 3)


def run_tests():
    from tests import suite
    return suite()

tests_require = [
    'nose',
    'unittest2',
]

install_requires = [
    "fabric==1.4.3",
    "Jinja2==2.6",
    "PyYAML==3.10"]

if not (is_py3 or (is_py2 and py_ver[1] >= 7)):
    install_requires.append("importlib==1.0.2")


setup(
    name="fabmagic",
    version=VERSION,
    description="Collection of python fabric recipes",
    long_description=readme_content,
    author="Alex Lispython",
    author_email="alex@obout.ru",
    maintainer="Alexandr Lispython",
    maintainer_email="alex@obout.ru",
    url="https://github.com/Lispython/",
    packages=["fabmagic",
              "fabmagic.frameworks",
              "fabmagic.ext"],
    include_package_data=True,
    package_data={
        'fabmagic': [
            'magic_templates/*',
        ]},
    install_requires=install_requires,
    tests_require=tests_require,
    license="BSD",
    platforms = ['Linux', 'Mac', 'Windows'],
    classifiers=[
         ## "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        ## "Development Status :: 3 - Alpha",
        ## "Development Status :: 4 - Beta",
        ## "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: System :: Clustering",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        ],
    test_suite = '__main__.run_tests'
    )
