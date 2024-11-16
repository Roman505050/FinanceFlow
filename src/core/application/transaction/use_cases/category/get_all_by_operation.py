from uuid import UUID

from core.application.transaction.dto.category import CategoryDTO
from core.domain.transaction.repositories.category import ICategoryRepository


class GetAllCategoriesByOperationUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, operation_id: UUID) -> list[CategoryDTO]:
        """Get all categories by operation.

        :return The categories.
        """
        entities = await self._category_repository.get_by_operation_id(
            operation_id=operation_id
        )
        return [CategoryDTO.from_entity(entity) for entity in entities]
