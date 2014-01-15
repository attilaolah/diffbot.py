# -*- coding: utf-8 -*-
"""Python client for the Diffbot API."""

from setuptools import find_packages, setup


setup(
    name='diffbot',
    version='1.0.0',
    url='http://www.diffbot.com/',
    license='MIT',
    author='Attila Oláh <attilaolah@gmail.com>',
    description="Python client for the Diffbot API.",
    packages=find_packages('.'),
    package_dir={'': '.'},
    include_package_data=False,
    test_suite='nose.collector',
    zip_safe=True,
    use_2to3=True,
)
