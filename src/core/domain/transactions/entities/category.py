from dataclasses import dataclass
from uuid import UUID

from core.domain.transactions.entities.operation import OperationEntity


@dataclass
class CategoryEntity:
    category_id: UUID
    category_name: str
    operation_type: OperationEntity
