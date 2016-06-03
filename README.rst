scopelist
=========

|build-status| |license|

*scopelist* exposes the ``ScopeList`` class, a container type intended to
simplify checking authorization scope.

Installation
------------

You can install scopelist directly from GitHub::

    > pip install git+https://github.com/te-je/scopelist

That should install all the dependencies for you. If you want to install
directly from source, clone the git repository and run the standard
`python setup.py install` command.

Dependencies
~~~~~~~~~~~~

* Python 2.7, 3.2+

Usage
-----

.. include:: scopelist.py
   :start-after: """Helper class for checking scope items.
   :end-before: """

.. That's the only docstring in the module, so we should be good.

.. |build-status| image:: https://travis-ci.org/te-je/scopelist.svg?branch=develop
    :target: https://travis-ci.org/te-je/scopelist
    :alt: build status
    :scale: 100%

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/te-je/scopelist/develop/LICENSE.rst
    :alt: License
    :scale: 100%
