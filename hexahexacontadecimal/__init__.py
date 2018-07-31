#!/usr/bin/env python
# -*- coding: utf8 -*-

"""**The most compact way to encode a number into a URL.**

Hexahexacontadecimal is a compact format to express a number or binary data in a URL. It uses all characters allowed in
a URL -- the [unreserved characters](http://tools.ietf.org/html/rfc3986#section-2.3) -- making it the most concise
way to express a positive integer in a URL.

Note that `urllib.quote` [escapes the tilde character (~)](http://bugs.python.org/issue16285), which is not necessary as
of RFC3986, so if you use this on HHC data you'll waste bytes. Use the provided `hhc_url_quote` function instead if you
must. By definition though HHC values don't need any URL quoting.

## Usage

    >>> from hexahexacontadecimal import hhc, hhc_to_int
    >>> print(hhc(302231454903657293676544))
    iFsGUkO.0tsxw
    >>> print(hhc_to_int('iFsGUkO.0tsxw'))
    302231454903657293676544

### Hexahexacontadecimal vs Base64 in URLs

    >>> n = 292231454903657293676544
    >>> import base64
    >>> print(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n))))
    PeHmHzZFTcAAAA%3D%3D
    >>> print(hhc_url_quote(hhc(n)))
    gpE4Xoy7fw5AO

Base64 vs HHC in a bad case for Base64:

    >>> n = 64 ** 5 + 1
    >>> print(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n))))
    QAAAAQ%3D%3D
    >>> print(hhc(n))
    ucrDZ

Base64 vs HHC in a bad case for HHC:

    >>> n = 66 ** 5 + 1
    >>> print(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n))))
    SqUUIQ%3D%3D
    >>> print(hhc(n))
    100001

That big SHA-512 you always wanted to write in a URL:

    >>> n = 2 ** 512
    >>> print(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n))))
    AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%3D
    >>> print(hhc(n))
    JK84xqGD9FMXPNubPghADlRhBUzlqRscC2h~8xmi99PvuQsUCIB2CHGhMUQR8FLm72.Hbbctkqi89xspay~y4

Massive savings!

### Are the savings really significant?

If you're currently doing your Base64 encoding the naive way, then yes. Encoding all numbers up to 100000, HHC will lead
to much shorter total length of URLs.

    >>> sum(len(hhc_url_quote(base64.urlsafe_b64encode(long_to_binary(n)))) for n in range(10 ** 5))
    531584
    >>> sum(len(hhc_url_quote(hhc(n))) for n in range(10 ** 5))
    295578

#### What if I use Base64 without padding?

Then the savings are much less significant. Yet they are still savings. If you're a perfectionist this is the kind of
thing you might care about.

Let's test it using the code from [this StackOverFlow question](http://stackoverflow.com/a/561704/76900):

    >>> from hexahexacontadecimal.num_encode_base64 import num_encode as num_encode_base64
    >>> n = 64 ** 5 + 1
    >>> print(hhc_url_quote(num_encode_base64(n)))
    BAAAAB
    >>> from hexahexacontadecimal.num_encode_base64 import num_decode as num_decode_base64
    >>> num_decode_base64(hhc_url_quote(num_encode_base64(n))) == n
    True

    >>> print(hhc(n))
    ucrDZ
    >>> hhc_to_int(hhc(n)) == n
    True

    >>> n = 66 ** 5 + 1
    >>> print(hhc_url_quote(num_encode_base64(n)))
    BKpRQh
    >>> print(hhc_url_quote(hhc(n)))
    100001

    >>> n = 2 ** 512
    >>> hhc_url_quote(num_encode_base64(n))
    'EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    >>> print(hhc_url_quote(hhc(n)))
    JK84xqGD9FMXPNubPghADlRhBUzlqRscC2h~8xmi99PvuQsUCIB2CHGhMUQR8FLm72.Hbbctkqi89xspay~y4

    >>> sum(len(hhc_url_quote(num_encode_base64(n))) for n in range(10 ** 5))
    295840
    >>> sum(len(hhc_url_quote(hhc(n))) for n in range(10 ** 5))
    295578

Why settle for less than perfect?

### Sorting

If you wish to be able to sort a list of HHC values numerically there is a variant of HHC that allows this. See
`sortable_hhc`.

    >>> hhc(67) < hhc(128)
    False
    >>> sortable_hhc(67, width=2) < sortable_hhc(128, width=2)
    True

### Negative Numbers

HHC expresses negative numbers by prefixing the number with `,` (since minus is taken). This is not a URL safe character
so if you URL encode a negative number with HHC you end up with `%2C` which takes up 2 extra characters. For this reason
HHC is not necessarily the shortest representation of a negative number.

The sortable variant also supports negative numbers and will yield the natural sort order (small to large),
like -2, -1, 0, 1, 2.

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import codecs
from io import StringIO

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

__all__ = ['hhc', 'hhc_to_int', 'hhc_url_quote', 'sortable_hhc', 'sortable_hhc_to_int']

NEGATIVE_PREFIX = ","
BASE66_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~"
SORTABLE_BASE66_ALPHABET = "-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~"
BASE = len(BASE66_ALPHABET)


def hhc_url_quote(s, safe=None):
    """Like urllib.parse.quote() but don't escape ~, in accordance with RFC3986.

    >>> print(hhc_url_quote(hhc(65)))
    ~
    """

    return quote(s, safe='~' + (safe or ''))


def long_to_binary(n):
    """Take an integer and write it as a binary string.

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
    """Take a binary string and read it as an integer.

    >>> binary_to_long(b'\\x00')
    0
    >>> binary_to_long(b'\\xff')
    255
    >>> binary_to_long(b'\\x02\\x03')
    515
    """

    return int(codecs.encode(b, 'hex'), 16)


def hhc(n, alphabet=BASE66_ALPHABET):
    """Represent a number in hexahexacontadecimal, a compact ASCII format of unreserved URL characters.

    >>> print(hhc(0))
    0
    >>> print(hhc(1))
    1
    >>> print(hhc(65))
    ~
    >>> print(hhc(66))
    10
    >>> print(hhc(67))
    11
    >>> print(hhc(302231454903657293676544))
    iFsGUkO.0tsxw

    Negative numbers are not URL safe and should be avoided:
    >>> print(hhc(-67))
    ,11

    """

    if n == 0:
        return alphabet[0]

    if n < 0:
        return NEGATIVE_PREFIX + hhc(-n, alphabet=alphabet)

    r = StringIO()
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
    >>> print(hhc_to_int('iFsGUkO.0tsxw'))
    302231454903657293676544
    >>> hhc_to_int(',11')
    -67

    """

    if s == '' or s is None:
        raise ValueError("invalid literal for hhc_to_int: {}".format(s))

    if s[0] == NEGATIVE_PREFIX:
        return -hhc_to_int(s[1:], alphabet=alphabet)

    n = 0

    for c in s:
        n = n * BASE + alphabet.index(c)

    return n


def sortable_hhc(n, width=0, alphabet=SORTABLE_BASE66_ALPHABET):
    """

    Represent a number in sortable hexahexacontadecimal, a compact format of unreserved URL characters which sorts
    the same alphabetically as numerically.

    This version is incompatible with standard HHC and it's a little less "user friendly". With regular HHC counting
    goes "0", "1", "2", ... "10", "11", "12"... which looks nice and natural. With sortable_hhc the same series is
    "-", ".", ".-", ".." which looks like some kind of morse code.

    >>> print(sortable_hhc(0))
    -
    >>> print(sortable_hhc(1))
    .
    >>> print(sortable_hhc(65))
    ~
    >>> print(sortable_hhc(66))
    .-
    >>> print(sortable_hhc(67))
    ..
    >>> print(sortable_hhc(6700))
    .XW
    >>> print(sortable_hhc(302231454903657293676544))
    fDpEShMz-qput

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

    >>> print(sortable_hhc(67, width=4))
    --..
    >>> sorted([sortable_hhc(x, width=2) for x in range(512)]) == [sortable_hhc(x, width=2) for x in range(512)]
    True

    Negative numbers are supported and will work like you expect, sorting like -2, -1, 0, 1, 2. (Note that the alphabet
    is reversed for negative numbers.)

    >>> print(sortable_hhc(-67))
    ,zz
    >>> print(sortable_hhc(-6700))
    ,zST
    >>> sortable_hhc(-50, width=5) < sortable_hhc(-1, width=5)
    True
    >>> sortable_hhc(-1, width=5) < sortable_hhc(0, width=5)
    True
    >>> sortable_hhc(0, width=5) < sortable_hhc(1, width=5)
    True
    >>> sortable_hhc(1, width=5) < sortable_hhc(50, width=5)
    True
    >>> sorted([sortable_hhc(x, width=5) for x in range(-512, 512)]) == [sortable_hhc(x, width=5) for x in range(-512, 512)]
    True

    """

    if n < 0:
        return NEGATIVE_PREFIX + sortable_hhc(-n, width=width - 1, alphabet=alphabet[::-1])

    r = hhc(n, alphabet=alphabet)
    return r.rjust(width, alphabet[0]) if width else r


def sortable_hhc_to_int(s):
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
    >>> sortable_hhc_to_int('.XW')
    6700
    >>> sortable_hhc_to_int('----..')
    67
    >>> print(sortable_hhc_to_int('fDpEShMz-qput'))
    302231454903657293676544

    Negative numbers are supported.

    >>> sortable_hhc_to_int(',zST')
    -6700

    """

    if s == '' or s is None:
        raise ValueError("invalid literal for sortable_hhc_to_int: {}".format(s))

    if s[0] == NEGATIVE_PREFIX:
        return -hhc_to_int(s[1:], alphabet=SORTABLE_BASE66_ALPHABET[::-1])

    return hhc_to_int(s, SORTABLE_BASE66_ALPHABET)
