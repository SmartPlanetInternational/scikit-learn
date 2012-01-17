# Author: Olivier Grisel <olivier.grisel@ensta.org>
#
# License: BSD Style.

import numpy as np
from sklearn.utils.murmurhash import murmurhash3_32
from numpy.testing import assert_array_almost_equal
from nose.tools import assert_equal


def test_mmhash3_int():
    assert_equal(murmurhash3_32(3), 847579505)
    assert_equal(murmurhash3_32(3, seed=0), 847579505)
    assert_equal(murmurhash3_32(3, seed=42), -1823081949)

    assert_equal(murmurhash3_32(3, positive=False), 847579505)
    assert_equal(murmurhash3_32(3, seed=0, positive=False), 847579505)
    assert_equal(murmurhash3_32(3, seed=42, positive=False), -1823081949)

    assert_equal(murmurhash3_32(3, positive=True), 847579505L)
    assert_equal(murmurhash3_32(3, seed=0, positive=True), 847579505L)
    assert_equal(murmurhash3_32(3, seed=42, positive=True), 2471885347L)


def test_mmhash3_bytes():
    assert_equal(murmurhash3_32('foo', 0), -156908512)
    assert_equal(murmurhash3_32('foo', 42), -1322301282)

    assert_equal(murmurhash3_32('foo', 0, positive=True), 4138058784L)
    assert_equal(murmurhash3_32('foo', 42, positive=True), 2972666014L)


def test_mmhash3_unicode():
    assert_equal(murmurhash3_32(u'foo', 0), -156908512)
    assert_equal(murmurhash3_32(u'foo', 42), -1322301282)

    assert_equal(murmurhash3_32(u'foo', 0, positive=True), 4138058784L)
    assert_equal(murmurhash3_32(u'foo', 42, positive=True), 2972666014L)


def test_no_collision_on_byte_range():
    previous_hashes = set()
    for i in range(100):
        h = murmurhash3_32(' ' * i, 0)
        assert (h not in previous_hashes,
                "Found collision on growing empty string")


def test_uniform_distribution():
    n_bins, n_samples = 10, 100000
    bins = np.zeros(n_bins, dtype=np.float)

    for i in range(n_samples):
        bins[murmurhash3_32(i, positive=True) % n_bins] += 1

    means = bins / n_samples
    expected = np.ones(n_bins) / n_bins

    assert_array_almost_equal(means / expected, np.ones(n_bins), 2)
