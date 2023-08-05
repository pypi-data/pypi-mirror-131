#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""

import numpy as np
import pandas as pd

from pyxel.detectors import Detector


def assert_only_photon_modified(actual: Detector, other: Detector) -> None:
    """Check if only the 'photon' array is modified.

    Parameters
    ----------
    actual : Detector
        The object to check.
    other : Detector
        The other object to check

    Raises
    ------
    AssertionError
        If other array(s) is modified and not 'photon'.
    """
    if not isinstance(actual, Detector):
        raise TypeError("Expecting a `Detector` object for 'actual'.")

    if type(actual) != type(other):
        raise AssertionError("'actual' and 'other' and not from the same type.")

    pd.testing.assert_frame_equal(actual.charge.frame, other.charge.frame)
    np.testing.assert_equal(
        actual.pixel.array, other.pixel.array, err_msg="'pixel' is modified !"
    )
    np.testing.assert_equal(
        actual.signal.array, other.signal.array, err_msg="'signal' is modified !"
    )
    np.testing.assert_equal(
        actual.image.array, other.image.array, err_msg="'image' is modified !"
    )

    with np.testing.assert_raises(AssertionError):

        np.testing.assert_equal(actual.photon.array, other.photon.array)


def assert_only_signal_modified(actual: Detector, other: Detector) -> None:
    """Check if only the 'signal' array is modified.

    Parameters
    ----------
    actual : Detector
        The object to check.
    other : Detector
        The other object to check

    Raises
    ------
    AssertionError
        If other array(s) is modified and not 'signal'.
    """
    if not isinstance(actual, Detector):
        raise TypeError("Expecting a `Detector` object for 'actual'.")

    if type(actual) != type(other):
        raise AssertionError("'actual' and 'other' and not from the same type.")

    np.testing.assert_equal(
        actual.photon.array, other.photon.array, err_msg="'photon' is modified !"
    )
    pd.testing.assert_frame_equal(actual.charge.frame, other.charge.frame)
    np.testing.assert_equal(
        actual.pixel.array, other.pixel.array, err_msg="'pixel' is modified !"
    )
    np.testing.assert_equal(
        actual.image.array, other.image.array, err_msg="'image' is modified !"
    )

    with np.testing.assert_raises(AssertionError):
        np.testing.assert_equal(actual.signal.array, other.signal.array)
