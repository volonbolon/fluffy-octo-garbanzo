from table import Table
from record import Record
import pmf
from enum import Enum

class Pregnancy(Record):
    """Represents a pregnancy."""

class Pregnancies(Table):
    """Contains survey data about a Pregnancy."""
    class Lengths(Enum):
        EARLY = 0
        ON_TIME = 1
        LATE = 2

    def read_records(self, data_dir='.', n=None):
        filename = self.get_filename()
        self.read_file(data_dir, filename, self.get_fields(), Pregnancy, n)
        self.recode()

    def get_filename(self):
        return '2002FemPreg.dat'

    def get_fields(self):
        """Gets information about the fields to extract from the survey data.

        Documentation of the fields for Cycle 6 is at
        http://nsfg.icpsr.umich.edu/cocoon/WebDocs/NSFG/public/index.htm

        Returns:
            sequence of (name, start, end, type) tuples
        """
        return [
            ('caseid', 1, 12, int),
            ('nbrnaliv', 22, 22, int),
            ('babysex', 56, 56, int),
            ('birthwgt_lb', 57, 58, int),
            ('birthwgt_oz', 59, 60, int),
            ('prglength', 275, 276, int),
            ('outcome', 277, 277, int),
            ('birthord', 278, 279, int),
            ('agepreg', 284, 287, int),
            ('finalwgt', 423, 440, float),
        ]

    def recode(self):
        for rec in self.records:
            rec.live = rec.outcome == 1

            # divide mother's age by 100
            try:
                if rec.agepreg != 'NA':
                    rec.agepreg /= 100.0
            except AttributeError:
                pass

            # convert weight at birth from lbs/oz to total ounces
            # note: there are some very low birthweights
            # that are almost certainly errors, but for now I am not
            # filtering
            try:
                if (rec.birthwgt_lb != 'NA' and rec.birthwgt_lb < 20 and
                            rec.birthwgt_oz != 'NA' and rec.birthwgt_oz <= 16):
                    rec.totalwgt_oz = rec.birthwgt_lb * 16 + rec.birthwgt_oz
                else:
                    rec.totalwgt_oz = 'NA'
            except AttributeError:
                pass

    def partition_between_first_and_others(self):
        firsts = Pregnancies()
        others = Pregnancies()

        for p in self.records:
            if p.live:
                if p.birthord == 1:
                    firsts.add_record(p)
                else:
                    others.add_record(p)
        return (firsts, others)

    def count_lives(self):
        live = 0
        for p in self.records:
            if p.live:
                live += 1
        return  live

    def mean(self):
        table = Table()
        table.records = [p.prglength for p in self.records]
        return table.mean()

    def standard_deviation(self):
        table = Table()
        table.records = [p.prglength for p in self.records]
        return table.standard_deviation()

    def early(self, first=True):
        if first:
            first, _ = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in first.records]
        else:
            _, others = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_early = test_pmf.probability_in_range(37)

        return prob_early

    def on_time(self, first=True):
        if first:
            first, _ = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in first.records]
        else:
            _, others = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        prob_lower = test_pmf.probability_in_range(37)
        prob_upper = test_pmf.probability_in_range(40)
        prob_on_time = prob_upper - prob_lower

        return prob_on_time

    def late(self, first=True):
        if first:
            first, _ = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in first.records]
        else:
            _, others = self.partition_between_first_and_others()
            pr_lengths = [p.prglength for p in others.records]
        test_pmf = pmf.make_pmf_from_list(pr_lengths)
        longest = sorted(pr_lengths, reverse=True)[0]
        prob_lower = test_pmf.probability_in_range(40)
        prob_upper = test_pmf.probability_in_range(longest)
        prob_late = prob_upper - prob_lower

        return prob_late

    def relative_risk(self, length=Lengths.ON_TIME):
        if length is Pregnancies.Lengths.EARLY:
            prob_early_first = self.early(first=True)
            prob_early_others = self.early(first=False)
            relative_risk = (prob_early_first * 100.0) / (prob_early_others * 100.0)
        elif length is Pregnancies.Lengths.ON_TIME:
            prob_on_time_first = self.on_time(first=True)
            prob_on_time_others = self.on_time(first=False)
            relative_risk = (prob_on_time_first * 100.0) / (prob_on_time_others * 100.0)
        else:
            prob_late_first = self.late(first=True)
            prob_late_others = self.late(first=False)
            relative_risk = (prob_late_first * 100.0) / (prob_late_others * 100.0)
        rounded_relative_risk = round(relative_risk, 2)
        return rounded_relative_risk

