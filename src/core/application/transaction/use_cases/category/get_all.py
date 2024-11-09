from core.application.transaction.dto.category import CategoryDTO
from core.domain.transaction.repositories.category import ICategoryRepository


class GetAllUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self) -> list[CategoryDTO]:
        """Get all categories.

        :return: The categories.
        """
        entities = await self._category_repository.get_all()
        return [CategoryDTO.from_entity(entity) for entity in entities]
