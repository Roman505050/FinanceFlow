from uuid import uuid4

from core.domain.transaction.entities.category import CategoryEntity
from core.domain.transaction.entities.operation import OperationEntity


class CategoryFactory:
    @staticmethod
    def create(
        category_name: str, operation: OperationEntity
    ) -> CategoryEntity:
        return CategoryEntity(
            category_id=uuid4(),
            category_name=category_name,
            operation=operation,
        )
