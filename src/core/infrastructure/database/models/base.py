from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, DeclarativeBase

from typing import Annotated
import datetime


class Base(DeclarativeBase):
    pass


created_at = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), default=func.now()),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    ),
]
last_seen_at = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        default=func.now(),
    ),
]
