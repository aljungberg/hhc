#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Encode and decode hexahexacontadecimal numbers.

Hexahexacontadecimal is a compact format to express a number or binary data in a URL. It uses all characters allowed in
a URL without escaping -- the [unreserved characters](http://tools.ietf.org/html/rfc3986#section-2.3) -- making it the
shortest possible way to express an integer in a URL.

Note that `urllib.quote` [escapes the tilde character (~)](http://bugs.python.org/issue16285), which is not necessary as
of RFC3986. The `hhc_url_quote` function is provided to help with this.

## Usage

    from hexahexacontadecimal import hhc, hhc_to_int

    print hhc(302231454903657293676544)  # 'iFsGUkO.0tsxw'
    print hhc_to_int('iFsGUkO.0tsxw')    # 302231454903657293676544L

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

### Sorting

If you wish to be able to sort a list of HHC values numerically there is a variant of HHC that allows this. See `sortable_hhc`.

    >>> hhc(67) < hhc(128)
    False
    >>> sortable_hhc(67, width=2) < sortable_hhc(128, width=2)
    True

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import BytesIO
import urllib

__all__ = ['hhc', 'hhc_to_int', 'hhc_url_quote', 'sortable_hhc', 'sortable_hhc_to_int']

BASE66_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~"
SORTABLE_BASE66_ALPHABET = b"-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~"
BASE = len(BASE66_ALPHABET)


def hhc_url_quote(s, safe=None):
    """Like urllib.quote() but don't escape ~, in accordance with RFC3986.

    >>> hhc_url_quote(hhc(65))
    '~'
    """

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

    >>> binary_to_long(b'\\x00')
    0
    >>> binary_to_long(b'\\xff')
    255
    >>> binary_to_long(b'\\x02\\x03')
    515
    """

    return int(b.encode('hex'), 16)


def hhc(n, alphabet=BASE66_ALPHABET):
    """Represent a number in hexahexacontadecimal, a compact ASCII format of unreserved URL characters.

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
        return alphabet[0]

    r = BytesIO()
    while n:
        n, t = divmod(n, BASE)
        r.write(alphabet[t])

    return r.getvalue()[::-1]


def hhc_to_int(s, alphabet=BASE66_ALPHABET):
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
        n = n * BASE + alphabet.index(c)

    return n


def sortable_hhc(n, width=0):
    """

    Represent a number in sortable hexahexacontadecimal, a compact format of unreserved URL characters which sorts
    the same alphabetically as numerically.

    This version is incompatible with standard HHC and it's a little less "user friendly". With regular HHC counting
    goes "0", "1", "2", ... "10", "11", "12"... which looks nice and natural. With sortable_hhc the same series is
    "-", ".", ".-", ".." which looks like some kind of morse code.

    >>> sortable_hhc(0)
    '-'
    >>> sortable_hhc(1)
    '.'
    >>> sortable_hhc(65)
    '~'
    >>> sortable_hhc(66)
    '.-'
    >>> sortable_hhc(67)
    '..'
    >>> sortable_hhc(302231454903657293676544)
    'fDpEShMz-qput'

    With standard HHC, alphabetical comparison is not the same as numeric comparison:
    >>> hhc(67) < hhc(128)
    False

    With sortable_hhc, two sortable_hhc numbers of the same width will compare the same as their numeric value.

    >>> sortable_hhc(67, width=2) < sortable_hhc(128, width=2)
    True
    >>> sorted([sortable_hhc(x) for x in range(66)]) == [sortable_hhc(x) for x in range(66)]
    True

    The width parameter allows you to set a minimum width. As long as that width is wider than you'll ever need,
    all generated values will sort alphabetically without decoding.

    >>> sortable_hhc(67, width=4)
    '--..'
    >>> sorted([sortable_hhc(x, width=2) for x in range(512)]) == [sortable_hhc(x, width=2) for x in range(512)]
    True

    """

    r = hhc(n, alphabet=SORTABLE_BASE66_ALPHABET)
    return r.rjust(width, SORTABLE_BASE66_ALPHABET[0]) if width else r


def sortable_hhc_to_int(s, alphabet=BASE66_ALPHABET):
    """Parse a number expressed in sortable hexahexacontadecimal as an integer (or long).

    >>> sortable_hhc_to_int('-')
    0
    >>> sortable_hhc_to_int('.')
    1
    >>> sortable_hhc_to_int('~')
    65
    >>> sortable_hhc_to_int('.-')
    66
    >>> sortable_hhc_to_int('..')
    67
    >>> sortable_hhc_to_int('----..')
    67
    >>> sortable_hhc_to_int('fDpEShMz-qput')
    302231454903657293676544L

    """

    return hhc_to_int(s, SORTABLE_BASE66_ALPHABET)
