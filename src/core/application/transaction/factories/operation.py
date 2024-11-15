from uuid import uuid4
from typing import Literal

from core.domain.transaction.entities.operation import OperationEntity
from core.domain.transaction.enums.operation import get_operation_type_enum


class OperationFactory:
    @staticmethod
    def create(
        operation_name: str,
        operation_type: Literal["income", "expense", "investment"],
    ) -> OperationEntity:
        return OperationEntity(
            operation_id=uuid4(),
            operation_name=operation_name,
            operation_type=get_operation_type_enum(operation_type),
        )
