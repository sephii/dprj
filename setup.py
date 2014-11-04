#!/usr/bin/env python
from setuptools import find_packages, setup
import sys

from setuptools.command.test import test as TestCommand

tests_require = [
    'pytest',
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='dprj',
    version='0.1.0',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    description='Double-metaphone-like algorithm for the french language',
    long_description=open("README.rst", 'rb').read().decode('utf-8'),
    author='Sylvain Fankhauser',
    author_email='sylvain@fankhauser.name',
    url='https://github.com/sephii/dprj',
    tests_require=tests_require,
    include_package_data=False,
    cmdclass = {'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 2.7",
    ],
)
