import sys

from collections import namedtuple
if sys.version_info < (3, 0):
    from collections import Iterable, Sequence
else:
    from collections.abc import Iterable, Sequence


__all__ = ['ScopeList']


class _ScopeItem(namedtuple("ScopeItem", "nodes modes")):
    def __new__(cls, item, child_sep, mode_sep, default_mode):
        node_part, _, mode_part = item.partition(mode_sep)

        if not mode_part:
            mode_part = default_mode

        return super(_ScopeItem, cls).__new__(
            cls, node_part.split(child_sep), set(mode_part))

    def as_string(self, child_sep, mode_sep, default_mode):
        if not self.modes or self.modes == set(default_mode):
            return child_sep.join(self.nodes)

        else:
            return mode_sep.join((child_sep.join(self.nodes),
                                  ''.join(sorted(self.modes))))


class ScopeList(Sequence):
    """Helper class for checking scope items.

    ScopeList implements the ``__contains__`` magic method, making it easy
    to check if a particular scope and permission is expressed a list of
    scopes.

    >>> from scopelist import ScopeList
    >>> ScopeList(['user/emails+r'])
    ScopeList(['user/emails'])
    >>> 'user/emails' in ScopeList(['user/emails'])
    True
    >>> ['foo/bar', 'foo/baz'] in ScopeList.from_string('foo')
    True
    >>> ['foo/bar', 'foo/baz', 'extra'] in ScopeList(['foo', 'bar'])
    False

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

    """

    def __init__(self, items,
                 child_sep="/", mode_sep="+", default_mode="r"):
        self.child_sep = child_sep
        self.mode_sep = mode_sep
        self.default_mode = default_mode

        self._items = tuple(
            _ScopeItem(item, self.child_sep, self.mode_sep, self.default_mode)
            for item in items
        )

    def __contains__(self, item):
        if not isinstance(item, str) and isinstance(item, Iterable):
            return all(o in self for o in item)

        _item = _ScopeItem(item, self.child_sep, self.mode_sep,
                           self.default_mode)

        for it in self._items:
            if _item.nodes[:len(it.nodes)] == it.nodes:
                # this is how many modes item has left to support
                _item.modes.difference_update(it.modes)

                if not _item.modes:
                    return True

        return False

    def __getitem__(self, i):
        return self._items[i].as_string(self.child_sep, self.mode_sep,
                                        self.default_mode)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "ScopeList([{}])".format(
            ", ".join(
                repr(item.as_string(self.child_sep, self.mode_sep,
                                    self.default_mode))
                for item in self._items
            )
        )

    @classmethod
    def from_string(cls, s, item_sep=" ", **args):
        """Get a new ScopeList from a string value"""
        items = [item for item in s.split(item_sep) if item]
        return cls(items, **args)
