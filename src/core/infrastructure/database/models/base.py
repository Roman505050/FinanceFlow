import datetime
from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


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
