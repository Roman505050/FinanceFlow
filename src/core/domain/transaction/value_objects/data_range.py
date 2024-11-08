from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class DataRange:
    start_date: datetime.date
    end_date: datetime.date

    def __eq__(self, other):
        return (
            self.start_date == other.start_date
            and self.end_date == other.end_date
        )

    def __ne__(self, other):
        return (
            self.start_date != other.start_date
            or self.end_date != other.end_date
        )
