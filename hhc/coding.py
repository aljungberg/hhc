#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from io import StringIO

NEGATIVE_PREFIX = ","
BASE = 66
HHC_ALPHABET = "-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~"
LEGACY_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.~"


def hhc(n, width=0, allow_special=False, alphabet=HHC_ALPHABET):
    """Represent a number in HHC, a compact ASCII numeral system using unreserved URL characters.

    >>> print(hhc(6700))
    .XW
    >>> print(hhc(302231454903657293676544))
    fDpEShMz-qput

    Two strings, `.` and `..`, have special meaning when used in URLs. For example, `example.com/a/..` is equivalent
    to `example.com/`. `hhc` avoids making these unless `allow_special` is True.

    >>> print(hhc(1))
    -.
    >>> print(hhc(67))
    -..
    >>> print(hhc(1, allow_special=True))
    .
    >>> print(hhc(67, allow_special=True))
    ..
    >>> hhc_to_int("-.") == hhc_to_int(".") and hhc_to_int("-..") == hhc_to_int("..")
    True

    (Both encodings are equivalent and decode to the same number.)

    HHC encoded numbers sort the same way alphabetically as numerically when the strings are of equal length. In other
    words, if x < y, then hhc(x) < hhc(y) if len(hhc(x)) == len(hhc(y)).

    If the strings are not guaranteed to be of equal length, you can still sort them without decoding by left padding
    them with `-` until they are.

    If you know the desired encoding length ahead of time and want to ensure sortability, use the `width` parameter:

    >>> hhc(67, width=3) < hhc(128, width=3)
    True
    >>> sorted([hhc(x, width=3) for x in range(512)]) == [hhc(x, width=3) for x in range(512)]
    True

    The width parameter, if given, must be 3 or greater unless allow_special=True.

    Negative numbers are supported. However, a non-URL safe prefix will be used, so you will need to URL encode the
    output. Sortability is preserved (-2, -1, 0, 1, 2).

    >>> print(hhc(-67))
    ,zz
    >>> print(hhc(-6700))
    ,zST
    >>> sorted([hhc(x, width=5) for x in range(-512, 512)]) == [hhc(x, width=5) for x in range(-512, 512)]
    True

    """

    if n < 0:
        return NEGATIVE_PREFIX + hhc(-n, width=width - 1, allow_special=True, alphabet=alphabet[::-1])

    r = hhc2(n, allow_special=allow_special, alphabet=alphabet)
    return r.rjust(width, alphabet[0]) if width else r


def hhc_to_int(s):
    """Parse a number expressed in sortable hhc as an integer (or long).

    >>> hhc_to_int('-')
    0
    >>> hhc_to_int('.')
    1
    >>> hhc_to_int('~')
    65
    >>> hhc_to_int('.-')
    66
    >>> hhc_to_int('..')
    67
    >>> hhc_to_int('.XW')
    6700
    >>> hhc_to_int('----..')
    67
    >>> print(hhc_to_int('fDpEShMz-qput'))
    302231454903657293676544

    Negative numbers are supported.

    >>> hhc_to_int(',zST')
    -6700

    """

    if s == '' or s is None or s[:2] == ',,':
        raise ValueError("invalid literal for hhc_to_int: {}".format(s))

    if s[0] == NEGATIVE_PREFIX:
        return -hhc2_to_int(s[1:], alphabet=HHC_ALPHABET[::-1])

    return hhc2_to_int(s, HHC_ALPHABET)


def hhc2(n, alphabet=LEGACY_ALPHABET, allow_special=True):
    """Represent a number in the HHC legacy format.

    This version of HHC is deprecated.

    >>> print(hhc2(0))
    0
    >>> print(hhc2(1))
    1
    >>> print(hhc2(65))
    ~
    >>> print(hhc2(66))
    10
    >>> print(hhc2(67))
    11
    >>> print(hhc2(302231454903657293676544))
    iFsGUkO.0tsxw

    Negative numbers are not URL safe and should be avoided:
    >>> print(hhc2(-67))
    ,11

    """

    if n == 0:
        return alphabet[0]

    if n < 0:
        return NEGATIVE_PREFIX + hhc2(-n, allow_special=True, alphabet=alphabet)

    r = StringIO()
    while n:
        n, t = divmod(n, BASE)
        r.write(alphabet[t])

    rv = r.getvalue()[::-1]

    if not allow_special and rv in ('.', '..'):
        return alphabet[0] + rv
    else:
        return rv


def hhc2_to_int(s, alphabet=LEGACY_ALPHABET):
    """Parse a number expressed in legacy HHC as an integer.

    This version of HHC is deprecated.

    >>> hhc2_to_int('0')
    0
    >>> hhc2_to_int('1')
    1
    >>> hhc2_to_int('~')
    65
    >>> hhc2_to_int('10')
    66
    >>> hhc2_to_int('11')
    67
    >>> print(hhc2_to_int('iFsGUkO.0tsxw'))
    302231454903657293676544
    >>> hhc2_to_int(',11')
    -67

    """

    if s == '' or s is None:
        raise ValueError("invalid literal for hhc2_to_int: {}".format(s))

    if s[0] == NEGATIVE_PREFIX:
        return -hhc2_to_int(s[1:], alphabet=alphabet)

    n = 0

    for c in s:
        n = n * BASE + alphabet.index(c)

    return n
