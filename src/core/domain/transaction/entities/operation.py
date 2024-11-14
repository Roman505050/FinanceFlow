from dataclasses import dataclass
from uuid import UUID


@dataclass
class OperationEntity:
    operation_id: UUID
    operation_name: str
    is_income: bool

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not 3 <= len(self.operation_name) <= 64:
            raise ValueError(
                "Category name must be between 3 and 64 characters"
            )
