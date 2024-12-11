import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class DataRange:
    start_date: datetime.date
    end_date: datetime.date
