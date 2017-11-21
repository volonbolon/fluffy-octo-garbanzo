from unittest import TestCase
from respondents import Respondents

class TestRespondents(TestCase):
    def test_read_records(self):
        resp = Respondents()
        resp.read_records()
        self.assertEqual(len(resp), 7643)