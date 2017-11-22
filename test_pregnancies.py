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
        early = pregs.early()
        self.assertEqual(early, 0.18241559030138227)

    def test_prob_first_on_time(self):
        pregs = Pregnancies()
        pregs.read_records()
        on_time = pregs.on_time()
        self.assertEqual(on_time, 0.6621346023113528)

    def test_prob_first_late(self):
        pregs = Pregnancies()
        pregs.read_records()
        prob_late = pregs.late()
        self.assertAlmostEqual(prob_late, 0.1554498074)

    def test_prob_others_early(self):
        pregs = Pregnancies()
        pregs.read_records()
        early = pregs.early(first=False)
        self.assertEqual(early, 0.16832101372756073)

    def test_prob_others_on_time(self):
        pregs = Pregnancies()
        pregs.read_records()
        on_time = pregs.on_time(first=False)
        self.assertEqual(on_time, 0.7379091869060191)

    def test_prob_others_late(self):
        pregs = Pregnancies()
        pregs.read_records()
        prob_late = pregs.late(first=False)
        self.assertAlmostEqual(prob_late, 0.0937697994)

    def test_relative_risk_early(self):
        pregs = Pregnancies()
        pregs.read_records()
        relative_risk = pregs.relative_risk(length=Pregnancies.Lengths.EARLY)
        self.assertAlmostEqual(relative_risk, 1.08) # +8%

    def test_relative_risk_on_time(self):
        pregs = Pregnancies()
        pregs.read_records()
        relative_risk = pregs.relative_risk(length=Pregnancies.Lengths.ON_TIME)
        self.assertAlmostEqual(relative_risk, 0.9) # -10%

    def test_relative_risk_late(self):
        pregs = Pregnancies()
        pregs.read_records()
        relative_risk = pregs.relative_risk(length=Pregnancies.Lengths.LATE)
        self.assertAlmostEqual(relative_risk, 1.66) # +66%

    def test_conditional_prob_first(self):
        pregs = Pregnancies()
        pregs.read_records()
        conditional_probability = pregs.conditional_probability(threshold=39, first=True)
        self.assertAlmostEqual(conditional_probability, 0.6336930455635491)