scopelist
=========

|build-status| |license| |coveralls| |pypi|

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

ScopeList implements the ``__contains__`` magic method, making it easy
to check if a particular scope and permission is expressed a list of
scopes.

>>> from scopelist import ScopeList
>>> ScopeList(['user/emails+r'])
ScopeList(['user/emails'])
>>> 'user/emails' in ScopeList(['user/emails'])
True

A ScopeList in fact works like any immutable sequence.

>>> len(ScopeList(['user/emails', 'user/repo']))
2
>>> ScopeList(['user/emails+r', 'user/repo+aaaaa'])[1]
'user/repo+a'
>>> list(ScopeList(['user/emails+r', 'user/repo+aaaaa']))
['user/emails', 'user/repo+a']

They can be parsed directly from strings too

>>> ScopeList.from_string("user/emails+r   user/emails+n")
ScopeList(['user/emails', 'user/emails+n'])

>>> ScopeList.from_string("user/emails+r:user/emails+n", item_sep=":")
ScopeList(['user/emails', 'user/emails+n'])

Permissions
~~~~~~~~~~~

You can append letters to scope items to express certain permissions.
Any ascii letter that follows the permission separator (``+`` by
default) is interpreted as a permission. When checking for an item
in the scope list, both its value and permission must match at least
one item in the list.

>>> 'user/emails+a' in ScopeList(['user/emails'])
False
>>> 'user/emails+a' in ScopeList(['user/emails+a'])
True

Indicate multiple permissions in a scope list item by including more than
one letter after the ``+`` symbol. Duplicate permissions are ignored.

>>> 'user/repo+w' in ScopeList(['user/repo+abcd', 'user/repo+rw'])
True

Permissions are totally arbitrary, except that ``+r`` is assumed by
default when no permissions are explicitly given.

>>> 'user/emails+r' in ScopeList(['user/emails'])
True

You can change the default permissions to whatever you like.

>>> 'user/emails+n' in ScopeList(['user/emails'], default_mode='n')
True
>>> 'user/emails+q' in ScopeList(['user/emails'], default_mode='pq')
True
>>> 'user/emails+p' in ScopeList(['user/emails'], default_mode='pq')
True

The permissions separator is also configurable.

>>> 'user/emails|r' in ScopeList(['user/emails'], mode_sep='|')
True

Parents
~~~~~~~

The ``/`` symbol is the default child separator. Parent scope items
automatically 'contain' child items in the scope list.

>>> 'user/emails+r' in ScopeList(['user'])
True
>>> 'user/emails+w' in ScopeList(['user'])
False
>>> 'user/emails+rw' in ScopeList(['user+w', 'user/emails+r'])
True

The child separator can also be changed:

>>> 'user:emails+r' in ScopeList(['user'], child_sep=':')
True

.. |build-status| image:: https://travis-ci.org/te-je/scopelist.svg?branch=develop
    :target: https://travis-ci.org/te-je/scopelist?branch=develop
    :alt: build status
    :scale: 100%

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/te-je/scopelist/develop/LICENSE.rst
    :alt: License
    :scale: 100%

.. |pypi| image:: https://img.shields.io/pypi/v/nine.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/scopelist
    :scale: 100%

.. |coveralls| image:: https://coveralls.io/repos/github/te-je/scopelist/badge.svg?branch=develop
    :target: https://coveralls.io/github/te-je/scopelist?branch=develop
