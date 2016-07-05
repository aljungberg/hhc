Hexahexacontadecimal
====================

**Hexahexacontadecimal is the most compact way to encode a number into a URL.**

Hexahexacontadecimal is a compact format to express a number or binary data in a URL. It uses all characters allowed in
a URL without escaping -- the [unreserved characters](http://tools.ietf.org/html/rfc3986#section-2.3) -- making it the
shortest possible way to express an integer in a URL.

Note that `urllib.quote` [escapes the tilde character (~)](http://bugs.python.org/issue16285), which is not necessary as
of RFC3986. The `hhc_url_quote` function is provided to help with this.

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

## Installation

    pip install hexahexacontadecimal

## Documentation

This file and docstrings.

## Tests

[![Build Status](https://travis-ci.org/aljungberg/hexahexacontadecimal.svg?branch=master)](https://travis-ci.org/aljungberg/hexahexacontadecimal)

To run the unit tests:

    nosetests --with-doctest

## Changelog

### 1.0

Initial release.

### 2.0

* New: sortable HHC. This variant of HHC sorts the same alphabetically as numerically for equal length strings.
* Shorter, more Pythonic method names. The main function is now simply called `hhc`, styled after Python's built in `hex` function. To decode the same, `hhc_to_int` is now used.
* `import * from hexahexacontadecimal` now only imports the main functions.
* `urlquote` was renamed to `hhc_url_quote` to make it easier to differentiate from the standard library method.

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
