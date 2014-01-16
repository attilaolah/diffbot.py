# -*- coding: utf-8 -*-
"""Python client for the Diffbot API."""
import sys
from setuptools import setup


PY_VERSION = sys.version_info[0], sys.version_info[1]

requirements = []

if PY_VERSION == (2, 6):
    requirements.append('argparse')


setup(
    name='diffbot',
    version='1.0.0',
    url='https://github.com/attilaolah/diffbot.py',
    license='MIT',
    author='Attila Oláh',
    author_email='attilaolah@gmail.com',
    description="Python client for the Diffbot API.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=requirements,
    tests_require=requirements+[
        "requests",
        "nose",
    ],
    py_modules=['diffbot'],
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'diffbot = diffbot:cli',
        ],
    },
    test_suite='nose.collector',
    zip_safe=True,
    use_2to3=True,
)
