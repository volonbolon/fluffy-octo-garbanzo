from table import Table
import record

class Respondent(record.Record):
    """Represents a respondent."""


class Respondents(Table):
    """Represents the respondent table."""

    def read_records(self, data_dir='.', n=None):
        filename = self.get_filename()
        self.read_file(data_dir, filename, self.get_fields(), Respondent, n)
        self.recode()

    def get_filename(self):
        return '2002FemResp.dat'

    def get_fields(self):
        """Returns a tuple specifying the fields to extract.

        The elements of the tuple are field, start, end, case.

                field is the name of the variable
                start and end are the indices as specified in the NSFG docs
                cast is a callable that converts the result to int, float, etc.
        """
        return [
            ('caseid', 1, 12, int),
        ]
