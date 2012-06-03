#!/usr/bin/python
# -*-python-*-
# This file is part of avahi.
#
# avahi is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# avahi is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with avahi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA.

import gdbm
import locale
import re

locale.setlocale(locale.LC_ALL, '')


class ServiceTypeDatabase:
    """ServiceTypeDatabase maps service types to descriptions"""

    def __init__(self, filename="/usr/lib/avahi/service-types.db"):
        self.db = gdbm.open(filename, "r")
        l = locale.getlocale(locale.LC_MESSAGES)
        self.suffixes = ()
        if not l[0] is None:
            if not l[1] is None:
                self.suffixes += (l[0] + "@" + l[1], )
            self.suffixes += (l[0], )
            i = l[0].find("_")
            if i >= 0:
                k = l[0][:i]
                if not l[1] is None:
                    self.suffixes += (k + "@" + l[1], )
                self.suffixes += (k, )

        self.suffixes = tuple(map(lambda x: "[" + x + "]",
                                  self.suffixes)) + ("", )

    def __getitem__(self, key):
        for suffix in self.suffixes:
            try:
                return self.db[key + suffix]
            except KeyError:
                pass
        raise KeyError()

    def items(self):
        return list(self.iteritems())

    def has_key(self, key):
        for suffix in self.suffixes:
            if key + suffix in self.db:
                return True
        return False

    def __contains__(self, item):
        for suffix in self.suffixes:
            if item + suffix in self.db:
                return True

        return False

    def __iter__(self):
        key = self.db.firstkey()
        while key is not None:
            if re.search('_[a-zA-Z0-9-]+\._[a-zA-Z0-9-]+', key) and \
               not re.search('_[a-zA-Z0-9-]+\._[a-zA-Z0-9-]+\[.*\]', key):
                yield key
            key = self.db.nextkey(key)

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        self.__len__ = lambda: count
        return len(self)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default

    def iteritems(self):
        return ((key, self[key]) for key in self)

    def iterkeys(self):
        return self.__iter__()

    def itervalues(self):
        return (self[key] for key in self)

    def keys(self):
        return list(self)

    def values(self):
        return list(self.itervalues())