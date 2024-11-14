from uuid import uuid4

from core.domain.transaction.entities.operation import OperationEntity


class OperationFactory:
    @staticmethod
    def create(operation_name: str, is_income: bool) -> OperationEntity:
        return OperationEntity(
            operation_id=uuid4(),
            operation_name=operation_name,
            is_income=is_income,
        )
