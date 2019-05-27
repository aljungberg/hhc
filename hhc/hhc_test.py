#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from nose.tools import eq_, ok_

from hhc import hhc_to_int, hhc2, hhc2_to_int
from . import hhc


def test_hhc__for_non_negative_numbers():
    eq_(hhc(0), '-')
    eq_(hhc(65), '~')
    eq_(hhc(66), '.-')
    eq_(hhc(6700), '.XW')
    eq_(hhc(302231454903657293676544), 'fDpEShMz-qput')


def test_hhc__for_negative_numbers():
    eq_(hhc(-67), ',zz')
    eq_(hhc(-6700), ',zST')
    eq_(hhc(-302231454903657293676544), ',Jl9kXHc.~8945')


def test_hhc__without_allow_special__should_pad_specials():
    eq_(hhc(1), '-.')
    eq_(hhc(67), '-..')


def test_hhc__with_allow_special__should_not_pad_specials():
    eq_(hhc(1, allow_special=True), '.')
    eq_(hhc(67, allow_special=True), '..')


def test_hhc2__without_allow_special__should_pad_specials():
    eq_(hhc2(64, allow_special=False), '0.')
    eq_(hhc2(4288, allow_special=False), '0..')


def test_hhc__without_allow_special__should_not_pad_specials():
    eq_(hhc2(64), '.')
    eq_(hhc2(4288), '..')


def test_hhc__with_negative_number__should_not_pad_specials():
    eq_(hhc(-64, allow_special=False), ',.')
    eq_(hhc(-4288, allow_special=False), ',..')


def test_hhc_to_int():
    eq_(hhc_to_int('-'), 0)
    eq_(hhc_to_int('~'), 65)
    eq_(hhc_to_int('.-'), 66)
    eq_(hhc_to_int('.XW'), 6700)
    eq_(hhc_to_int('fDpEShMz-qput'), 302231454903657293676544)
    eq_(hhc_to_int(',~'), 0)  # negative zero
    eq_(hhc_to_int(',zz'), -67)
    eq_(hhc_to_int(',zST'), -6700)
    eq_(hhc_to_int(',Jl9kXHc.~8945'), -302231454903657293676544)


def test_hhc2_to_int():
    eq_(hhc2_to_int('0'), 0)
    eq_(hhc2_to_int('-'), 62)
    eq_(hhc2_to_int('~'), 65)
    eq_(hhc2_to_int('.'), 64)
    eq_(hhc2_to_int('0.'), 64)
    eq_(hhc2_to_int('..'), 4288)
    eq_(hhc2_to_int('0..'), 4288)
    eq_(hhc2_to_int('.-'), 4286)
    eq_(hhc2_to_int('.XW'), 280994)
    eq_(hhc2_to_int('fDpEShMz-qput'), 281524654803017445463699)
    eq_(hhc2_to_int(',0'), 0)  # negative zero
    eq_(hhc2_to_int(',zz'), -4087)
    eq_(hhc2_to_int(',zST'), -267593)
    eq_(hhc2_to_int(',fDpEShMz-qput'), -281524654803017445463699)


def test_hhc_to_int__double_minus__should_crash():
    # Because the result would be undefined.
    try:
        hhc_to_int(',,zz')
        ok_(False, ",, shouldn't be allowed")
    except ValueError as e:
        pass


def test_hhc__alphabetic_sort_should_be_equivalent_to_numeric_sort():
    values = [hhc(x, width=3) for x in range(-512, 512)]
    eq_(values, sorted(values))


def test_hhc__without_width_param__should_be_sortable_anyhow_with_manual_padding():
    values = [hhc(x).rjust(3, '-') for x in range(0, 512)]
    eq_(values, sorted(values))


def test_hhc__for_negative_numbers_without_width_param__should_be_sortable_anyhow_with_manual_padding():
    values = [hhc(x).rjust(3, '-') for x in range(-512, 512)]
    eq_(values, sorted(values))
