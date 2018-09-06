Hexahexacontadecimal
====================

**The most compact way to encode a number into a URL.**

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

## Installation

    pip install hexahexacontadecimal

## Documentation

This file and docstrings.

## Tests

[![Build Status](https://travis-ci.org/aljungberg/hexahexacontadecimal.svg?branch=master)](https://travis-ci.org/aljungberg/hexahexacontadecimal)

To run the unit tests:

    nosetests --with-doctest

## Changelog

### 2.2.1

* Fixed: pandoc accidentally required.

### 2.2

* Python 3 support (backwards compatible with Python 2.7).

### 2.1

* Fixed: `hhc(-1)` would cause an infinite loop.
* New: support for negative values.

### 2.0

* New: sortable HHC. This variant of HHC sorts the same alphabetically as numerically for equal length strings.
* Shorter, more Pythonic method names. The main function is now simply called `hhc`, styled after Python's built in `hex` function. To decode the same, `hhc_to_int` is now used.
* `import * from hexahexacontadecimal` now only imports the main functions.
* `urlquote` was renamed to `hhc_url_quote` to make it easier to differentiate from the standard library method.

### 1.0

Initial release.

## On the command line

With [pyle](https://github.com/aljungberg/pyle) you can easily use hexahexacontadecimal on the command line.

    $ wc -c LICENSE MANIFEST setup.py | pyle -m hexahexacontadecimal -e "'%-10s Hexhexconta bytes:' % words[1], hexahexacontadecimal.hhc(int(words[0]))"
    LICENSE    Hexhexconta bytes: MV
    MANIFEST   Hexhexconta bytes: 1z
    setup.py   Hexhexconta bytes: GI
    total      Hexhexconta bytes: ei

## License

Free to use and modify under the terms of the BSD open source license.

## Author

Alexander Ljungberg
