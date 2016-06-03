# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path


HERE = path.abspath(path.dirname(__file__))


def read(relpath):
    with open(path.join(HERE, relpath), encoding="utf-8") as f:
        return f.read()

setup(
    name='scopelist',

    description='A container class for authorization scopes',
    long_description=read("README.rst") + "License\n-------\n\n" + read("LICENSE.rst"),

    url='https://github.com/te-je/scopelist',

    author='Te-jé Rodgers',
    author_email='tjd.rodgers@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

    ],

    setup_requires=['setuptools_scm'],
    use_scm_version={"write_to": "scopelist/VERSION.txt"},

    packages=find_packages(exclude=['test']),
    install_requires=[],

    extras_require={
    },

    package_data={
        'scopelist': ['VERSION.txt'],
    },

    entry_points={
    },
)
