from dataclasses import dataclass
from uuid import UUID

from core.domain.transaction.value_objects.amount_range import AmountRange
from core.domain.transaction.value_objects.data_range import DataRange


@dataclass
class TransactionFilters:
    user_id: UUID | None = None
    currency_ids: list[UUID] | None = None
    operation_ids: list[UUID] | None = None
    category_ids: list[UUID] | None = None
    data_range: DataRange | None = None
    amount_range: AmountRange | None = None
