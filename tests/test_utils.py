import numpy as np
from scipy.signal import ricker, find_peaks
import unittest


from blockhead.util import create_scale_space, harmonic_average


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.series = np.zeros(1023)
        self.series[[256, 512, 768]] = 1

    def test_create_scale_space(self):
        scale_space = create_scale_space(self.series, max_scale=10)

        for idx in range(10):
            scale = scale_space['scales'][idx]

            a = scale_space['second'][:, idx]
            b = -ricker(1023, scale)

            # normalization doesn't matter:
            comp = np.convolve(self.series, b, mode='same')

            np.testing.assert_array_equal(
                find_peaks(-a)[0],
                find_peaks(-comp)[0]
            )

            np.testing.assert_array_equal(
                find_peaks(a)[0],
                find_peaks(comp)[0]
            )

    def test_harmonic_average(self):
        self.assertEqual(
            3/(1/1 + 1/2 + 1/3),
            harmonic_average(np.array([1, 2, 3]))
        )
