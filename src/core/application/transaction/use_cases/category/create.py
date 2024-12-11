from uuid import uuid4

from core.application.transaction.dto.category import (
    CategoryDTO,
    CreateCategoryDTO,
)
from core.domain.transaction.entities.category import CategoryEntity
from core.domain.transaction.repositories.category import ICategoryRepository
from core.domain.transaction.repositories.operation import IOperationRepository


class CreateCategoryUseCase:
    def __init__(
        self,
        category_repository: ICategoryRepository,
        operation_repository: IOperationRepository,
    ):
        self._category_repository = category_repository
        self._operation_repository = operation_repository

    async def execute(self, request: CreateCategoryDTO) -> CategoryDTO:
        """
        Create a operation.

        :arg request: The request data.
        :raise OperationNotFoundException: If the operation does not exist.
        :raise CategoryAlreadyExistsException: If the operation already exists.
        :return: The created operation.
        """
        operation = await self._operation_repository.get_by_id(
            request.operation_id
        )

        category = CategoryEntity(
            category_id=uuid4(),
            category_name=request.category_name,
            operation=operation,
        )

        category = await self._category_repository.save(category)

        return CategoryDTO.from_entity(category)
