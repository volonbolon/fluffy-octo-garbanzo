from unittest import TestCase
import pmf
import plot


class TestPMF(TestCase):
    def test_make_PMF_from_list(self):
        hist = pmf.make_hist_from_list([1, 2, 2, 3, 5])
        self.assertEqual(hist.freq(2), 2)

    def test_mode(self):
        hist = pmf.make_hist_from_list([1, 2, 2, 2, 3, 5])
        mode = hist.mode()
        self.assertEqual(mode, 2)

    def test_all_modes(self):
        hist = pmf.make_hist_from_list([1, 2, 5, 2, 2, 1, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5])
        mode = hist.all_modes()
        self.assertEqual(mode, [(5, 7), (3, 4), (2, 3), (1, 2)])

    def test_probability_in_range(self):
        test_pmf = pmf.make_pmf_from_list([1, 2, 5, 2, 2, 1, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5])
        prob_in_range = test_pmf.probability_in_range(3)
        self.assertEqual(prob_in_range, 0.5625)