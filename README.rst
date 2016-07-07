scopes
=========

|build-status| |license| |coveralls| |pypi|

*scopes* exposes the ``Set`` class, a container type intended to
simplify checking authorization scope.

Installation
------------

You can install scopes from PyPi::

    > pip install scopes

That should install all the dependencies for you. If you want to install
directly from source, clone the git repository and run the standard
`python setup.py install` command.

Dependencies
~~~~~~~~~~~~

* Python 2.7, 3.2+

Usage
-----

scopes.Set implements the ``__contains__`` magic method, making it easy
to check if a particular scope and permission is expressed in a set of
scopes.

>>> from scopes import Set
>>> Set(['user/emails+r'])
Set(['user/emails'])
>>> 'user/emails' in Set(['user/emails'])
True
>>> ('foo/bar', 'foo/baz') <= Set('foo')
True
>>> ['foo/bar', 'foo/baz', 'extra'] <= Set(['foo', 'bar'])
False
>>> Set(['foo', 'bar']) >= ('foo/bar', 'foo/baz')
True

A Set in fact works almost like any set type.

>>> len(Set(['user/emails', 'user/repo']))
2
>>> list(Set(['user/emails+r', 'user/repo+aaaaa']).formatted())
['user/emails', 'user/repo+a']

They can be quickly parsed from strings too.

>>> Set("user/emails+r user/emails+n")
Set(['user/emails', 'user/emails+n'])

This method uses a single space as a separator.

Permissions
~~~~~~~~~~~

You can append letters to scope items to express certain permissions.
Any ascii letter that follows the permission separator (``+`` by
default) is interpreted as a permission. When checking for an item
in the scope list, both its value and permission must match at least
one item in the list.

>>> 'user/emails+a' in Set(['user/emails'])
False
>>> 'user/emails+a' in Set(['user/emails+a'])
True

Indicate multiple permissions in a scope list item by including more than
one letter after the ``+`` symbol. Duplicate permissions are ignored.

>>> 'user/repo+w' in Set(['user/repo+abcd', 'user/repo+rw'])
True

Permissions are totally arbitrary, except that ``+r`` is assumed by
default when no permissions are explicitly given.

>>> 'user/emails+r' in Set(['user/emails'])
True

You can change the default permissions to whatever you like.

>>> 'user/emails+n' in Set(['user/emails'], default_permissions='n')
True
>>> 'user/emails+q' in Set(['user/emails'], default_permissions='pq')
True
>>> 'user/emails+p' in Set(['user/emails'], default_permissions='pq')
True

The permissions separator is also configurable.

>>> 'user/emails|r' in Set(['user/emails'], permission_sep='|')
True

Parents
~~~~~~~

The ``/`` symbol is the default child separator. Parent scope items
automatically 'contain' child items in the scope list.

>>> 'user/emails+r' in Set(['user'])
True
>>> 'user/emails+w' in Set(['user'])
False
>>> 'user/emails+rw' in Set(['user+w', 'user/emails+r'])
True

The child separator can also be changed:

>>> 'user:emails+r' in Set(['user'], child_sep=':')
True

.. |build-status| image:: https://travis-ci.org/te-je/scopes.svg?branch=develop
    :target: https://travis-ci.org/te-je/scopes?branch=develop
    :alt: build status
    :scale: 100%

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/te-je/scopes/develop/LICENSE.rst
    :alt: License
    :scale: 100%

.. |pypi| image:: https://img.shields.io/pypi/v/scopes.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/scopes
    :scale: 100%

.. |coveralls| image:: https://coveralls.io/repos/github/te-je/scopes/badge.svg?branch=develop
    :target: https://coveralls.io/github/te-je/scopes?branch=develop
