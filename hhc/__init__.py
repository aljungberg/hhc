#!/usr/bin/env python
# -*- coding: utf8 -*-

"""**The most compact way to encode a number into a URL.**

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import codecs

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from .coding import hhc, hhc_to_int, hhc2, hhc2_to_int


__all__ = ['hhc_url_quote', 'hhc', 'hhc_to_int', 'hhc2', 'hhc2_to_int']


def hhc_url_quote(s, safe=None):
    """Like urllib.parse.quote() but don't escape ~, in accordance with RFC3986.

    >>> print(hhc_url_quote(hhc2(65)))
    ~
    """

    return quote(s, safe='~' + (safe or ''))


def long_to_binary(n):
    """Helper method to express an integer as binary data.

    >>> long_to_binary(0) == b'\\x00'
    True
    >>> long_to_binary(255) == b'\\xff'
    True
    >>> long_to_binary(512 + 3) == b'\\x02\\x03'
    True
    """

    if hasattr(n, 'to_bytes'):
        if n == 0:
            return b'\x00'

        return n.to_bytes((n.bit_length()+7)//8, 'big')
    else:
        # Python 2
        h = '%x' % n
        return ('0'*(len(h) % 2) + h).decode('hex')


def binary_to_long(b):
    """Helper method to interpret binary data as an integer.

    >>> binary_to_long(b'\\x00')
    0
    >>> binary_to_long(b'\\xff')
    255
    >>> binary_to_long(b'\\x02\\x03')
    515
    """

    return int(codecs.encode(b, 'hex'), 16)


