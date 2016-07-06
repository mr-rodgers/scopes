import sys

from collections import namedtuple
from itertools import chain, repeat
if sys.version_info < (3, 0):
    from collections import Set as AbstractSet
    texttype = (unicode, str)  # noqa
else:
    from collections.abc import Set as AbstractSet
    texttype = str


__all__ = ['Set', 'Item']


class Item(namedtuple("Item", "nodes permissions")):
    @classmethod
    def parse(cls, s, child_sep=u"/", permission_sep=u"+",
              default_permissions=u"r"):
        node_part, _, permission_part = s.partition(permission_sep)

        if not permission_part:
            permission_part = default_permissions

        return cls(node_part.split(child_sep), set(permission_part))

    def format(self, child_sep=u"/", permission_sep=u"+",
               default_permissions=u"r"):
        node_part = child_sep.join(self.nodes)
        permissions_part = u"".join(self.permissions)

        if permissions_part == default_permissions:
            return node_part

        else:
            return permission_sep.join((node_part, permissions_part))

    def parents(self, other):
        """
        Return whether this Item is a parent of another Item
        (ignores permissions)
        """
        return other.nodes[:len(self.nodes)] == self.nodes

    def rejects(self, other):
        """
        Return which permissions of the other item this does not provide
        """
        return other.permissions - self.permissions

    def __contains__(self, other):
        return self.parents(other) and not self.rejects(other)


class Set(AbstractSet):
    """Helper class for checking scope items.

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

    """
    def __init__(self, items, child_sep=u"/", permission_sep=u"+",
                 default_permissions=u"r"):
        self.child_sep = child_sep
        self.permission_sep = permission_sep
        self.default_permissions = default_permissions

        if isinstance(items, texttype):
            items = items.split()

        self.items = tuple(self._make_item(o) for o in items)

    def __contains__(self, item):
        # Coerce the argument to an Item instance
        item = self._make_item(item)

        # Find parent items, and for each one, mark the required permissions
        # that it provides as met
        parents = (o for o in self.items if o.parents(item))
        for parent in parents:
            unmet_permissions = parent.rejects(item)

            # If all the permissions have been met, time to go
            if not unmet_permissions:
                return True

            else:
                # update item so that it only looks for those missing
                # permissions; not ones which have already been met
                item = Item(item.nodes, unmet_permissions)

        else:
            # The entire set of parents is traversed, but there are
            # unmet permissions
            return False

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return "Set({!r})".format(list(self.formatted()))

    def __ge__(self, other):
        if not isinstance(other, Set):
            other = Set(other)

        self = self._expanded_to_match(other)

        return super(Set, self).__ge__(other)

    def _expanded_to_match(self, other):
        # In order to get around an optimisation by collections.abc.Set,
        # must make sure the other is not larger that this, even if it
        # means adding dummy items
        o = self
        differential = len(other) - len(o)

        if differential > 0:
            dummy = Item([], set())
            o = Set(chain(o.items, repeat(dummy, differential)))

        return o

    def formatted(self):
        for item in self.items:
            yield item.format(
                child_sep=self.child_sep,
                permission_sep=self.permission_sep,
                default_permissions=self.default_permissions
            )

    def _make_item(self, o):
        # Convert an object to an item if it isn't already
        if isinstance(o, Item):
            return o

        elif isinstance(o, texttype):
            return Item.parse(
                o,
                child_sep=self.child_sep,
                permission_sep=self.permission_sep,
                default_permissions=self.default_permissions
            )

        else:
            raise TypeError("object not supported scope item: {0}".format(o))
