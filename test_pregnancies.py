from unittest import TestCase
from pregnancies import Pregnancies
import pmf

class TestPregnancies(TestCase):
    def test_read_records(self):
        resp = Pregnancies()
        resp.read_records()
        self.assertEqual(len(resp), 13593)

    def test_count_live(self):
        resp = Pregnancies()
        resp.read_records()
        self.assertEqual(resp.count_lives(), 9148)

    def test_partition(self):
        pregs = Pregnancies()
        pregs.read_records()
        firsts, others = pregs.partition_between_first_and_others()
        self.assertEqual(len(firsts), 4413)
        self.assertEqual(len(others), 4735)

    def test_mean_firsts(self):
        pregs = Pregnancies()
        pregs.read_records()
        firsts, _ = pregs.partition_between_first_and_others()
        self.assertEqual(firsts.mean(), 38.60095173351461)

    def test_mean_others(self):
        pregs = Pregnancies()
        pregs.read_records()
        _, others = pregs.partition_between_first_and_others()
        self.assertEqual(others.mean(), 38.52291446673706)

    def test_sigma_firsts(self):
        pregs = Pregnancies()
        pregs.read_records()
        firsts, _ = pregs.partition_between_first_and_others()
        self.assertEqual(firsts.standard_deviation(), 2.7915850698243654)

    def test_sigma_others(self):
        pregs = Pregnancies()
        pregs.read_records()
        _, others = pregs.partition_between_first_and_others()
        self.assertEqual(others.standard_deviation(), 2.6155761106844913)

    def test_prob_first_early(self):
        pregs = Pregnancies()
        pregs.read_records()
        first, _ = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in first.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_in_range = test_pmf.probability_in_range(37)
        self.assertEqual(prob_in_range, 0.18241559030138227)

    def test_prob_first_on_time(self):
        pregs = Pregnancies()
        pregs.read_records()
        first, _ = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in first.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_lower = test_pmf.probability_in_range(37)
        prob_upper = test_pmf.probability_in_range(40)
        prob_on_time = prob_upper - prob_lower
        self.assertEqual(prob_on_time, 0.6621346023113528)

    def test_prob_first_late(self):
        pregs = Pregnancies()
        pregs.read_records()
        first, _ = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in first.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        longest = sorted(pr_lengths, reverse=True)[0]
        prob_lower = test_pmf.probability_in_range(40)
        prob_upper = test_pmf.probability_in_range(longest)
        prob_late = prob_upper - prob_lower
        self.assertAlmostEqual(prob_late, 0.1554498074)

    def test_prob_others_early(self):
        pregs = Pregnancies()
        pregs.read_records()
        _, others = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_in_range = test_pmf.probability_in_range(37)
        self.assertEqual(prob_in_range, 0.16832101372756073)

    def test_prob_first_on_time(self):
        pregs = Pregnancies()
        pregs.read_records()
        _, others = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_lower = test_pmf.probability_in_range(37)
        prob_upper = test_pmf.probability_in_range(40)
        prob_on_time = prob_upper - prob_lower
        self.assertEqual(prob_on_time, 0.7379091869060191)

    def test_prob_first_late(self):
        pregs = Pregnancies()
        pregs.read_records()
        _, others = pregs.partition_between_first_and_others()
        pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        longest = sorted(pr_lengths, reverse=True)[0]
        prob_lower = test_pmf.probability_in_range(40)
        prob_upper = test_pmf.probability_in_range(longest)
        prob_late = prob_upper - prob_lower
        self.assertAlmostEqual(prob_late, 0.0937697994)
