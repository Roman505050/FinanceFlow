from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class DataRange:
    start_date: datetime.date
    end_date: datetime.date
