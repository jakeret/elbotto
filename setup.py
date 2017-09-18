#!/usr/bin/env python

import os
import sys
from setuptools.command.test import test as TestCommand
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


readme = open('README.rst').read()

history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requires = ["websocket-client", "mock"] #during runtime
tests_require=['pytest>=2.3'] #for testing

PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name='elbotto',
    version='0.1.0',
    description='Jass bot skeleton',
    long_description=readme + '\n\n' + history,
    author='Joel Akeret',
    author_email='joel.akeret@zuehlke.com',
    url='https://github.com/jakeret/elbotto',
    packages=find_packages(PACKAGE_PATH, "test"),
    package_dir={'elbotto': 'elbotto'},
    include_package_data=True,
    install_requires=requires,
    license='GPLv3',
    zip_safe=False,
    keywords='elbotto',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=tests_require,
    cmdclass = {'test': PyTest},
)
