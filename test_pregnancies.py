from unittest import TestCase
from pregnancies import Pregnancies

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