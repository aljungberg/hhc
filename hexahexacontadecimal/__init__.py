#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Encode and decode hexahexacontadecimal numbers.

Hexahexacontadecimal is a compact format to express a number or binary data in a URL. It uses all characters allowed in
a URL without escaping -- the [unreserved characters](http://tools.ietf.org/html/rfc3986#section-2.3) -- making it the
shortest possible way to express an integer in a URL.

Note that `urllib.quote` [escapes the tilde character (~)](http://bugs.python.org/issue16285), which is not necessary as
of RFC3986.

### Hexahexacontadecimal vs Base64 in URLs

    >>> n = 292231454903657293676544
    >>> import base64
    >>> hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))
    'PeHmHzZFTcAAAA%3D%3D'
    >>> hhc_url_quote(hhc(n))
    'gpE4Xoy7fw5AO'

Worst case scenario for plain Base64:

    >>> n = 64 ** 5 + 1
    >>> hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))
    'QAAAAQ%3D%3D'
    >>> hhc_url_quote(hhc(n))
    'ucrDZ'

Worst case for hexahexacontadecimal:

    >>> n = 66 ** 5 + 1
    >>> hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))
    'SqUUIQ%3D%3D'
    >>> hhc_url_quote(hhc(n))
    '100001'

That big SHA-512 you always wanted to write in a URL:

    >>> n = 2 ** 512
    >>> hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))
    'AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%3D'
    >>> hhc_url_quote(hhc(n))
    'JK84xqGD9FMXPNubPghADlRhBUzlqRscC2h~8xmi99PvuQsUCIB2CHGhMUQR8FLm72.Hbbctkqi89xspay~y4'

Massive savings.

### Are the savings really significant?

If you're currently doing your Base64 encoding the naive way, then yes:

    >>> sum(len(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))) for n in xrange(10 ** 5))
    531584
    >>> sum(len(hhc_url_quote(hhc(n))) for n in xrange(10 ** 5))
    295578

### But what if I use Base64 without padding?

Then the savings are not as significant. But it's still an improvement. Using the code from [this StackOverFlow
question](http://stackoverflow.com/a/561704/76900):

    >>> from hexahexacontadecimal.num_encode_base64 import num_encode as num_encode_base64
    >>> n = 64 ** 5 + 1
    >>> hhc_url_quote(num_encode_base64(n))
    'BAAAAB'
    >>> hhc_url_quote(hhc(n))
    'ucrDZ'
    >>> n = 66 ** 5 + 1
    >>> hhc_url_quote(num_encode_base64(n))
    'BKpRQh'
    >>> hhc_url_quote(hhc(n))
    '100001'
    >>> n = 2 ** 512
    >>> hhc_url_quote(num_encode_base64(n))
    'EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    >>> hhc_url_quote(hhc(n))
    'JK84xqGD9FMXPNubPghADlRhBUzlqRscC2h~8xmi99PvuQsUCIB2CHGhMUQR8FLm72.Hbbctkqi89xspay~y4'
    >>> sum(len(hhc_url_quote(num_encode_base64(n))) for n in xrange(10 ** 5))
    295840
    >>> sum(len(hhc_url_quote(hhc(n))) for n in xrange(10 ** 5))
    295578

Why settle for less than perfect?

"""

from __future__ import absolute_import, division, print_function

from io import StringIO
import urllib

__all__ = ['hhc', 'hhc_to_int', 'hhc_url_quote']

BASE66_ALPHABET = u"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~"
BASE = len(BASE66_ALPHABET)


def hhc_url_quote(s, safe=None):
    """Like urllib.quote() but don't escape ~, in accordance with RFC3986."""

    return urllib.quote(s, safe='~' + (safe or ''))


def long_to_binary(n):
    """Take an integer and write it as a binary string.

    >>> long_to_binary(0)
    '\\x00'
    >>> long_to_binary(255)
    '\\xff'
    >>> long_to_binary(512 + 3)
    '\\x02\\x03'
    """

    h = '%x' % n
    return ('0' * (len(h) % 2) + h).decode('hex')


def binary_to_long(b):
    """Take a binary string and read it as an integer.

    >>> binary_to_long('\\x00')
    0
    >>> binary_to_long('\\xff')
    255
    >>> binary_to_long('\\x02\\x03')
    515
    """

    return int(b.encode('hex'), 16)


def hhc(n):
    """Represent a number in hexahexacontadecimal, a compact format of unreserved URL characters.

    >>> hhc(0)
    '0'
    >>> hhc(1)
    '1'
    >>> hhc(65)
    '~'
    >>> hhc(66)
    '10'
    >>> hhc(67)
    '11'
    >>> hhc(302231454903657293676544)
    'iFsGUkO.0tsxw'

    """

    if n == 0:
        return BASE66_ALPHABET[0].encode('ascii')

    r = StringIO()
    while n:
        n, t = divmod(n, BASE)
        r.write(BASE66_ALPHABET[t])

    return r.getvalue().encode('ascii')[::-1]


def hhc_to_int(s):
    """Parse a number expressed in hexahexacontadecimal as an integer (or long).

    >>> hhc_to_int('0')
    0
    >>> hhc_to_int('1')
    1
    >>> hhc_to_int('~')
    65
    >>> hhc_to_int('10')
    66
    >>> hhc_to_int('11')
    67
    >>> hhc_to_int('iFsGUkO.0tsxw')
    302231454903657293676544L

    """

    n = 0
    for c in s:
        n = n * BASE + BASE66_ALPHABET.index(c)

    return n
