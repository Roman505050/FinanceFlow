from dataclasses import dataclass
from uuid import UUID

from core.domain.transaction.entities.operation import OperationEntity


@dataclass
class CategoryEntity:
    category_id: UUID
    category_name: str
    operation_type: OperationEntity

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not 3 <= len(self.category_name) <= 64:
            raise ValueError(
                "Category name must be between 3 and 64 characters"
            )
