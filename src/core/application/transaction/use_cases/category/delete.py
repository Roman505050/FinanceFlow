from uuid import UUID

from core.domain.transaction.repositories.category import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: UUID) -> None:
        """Delete a category.

        :arg category_id: The category ID.
        :raise CategoryNotFoundException: If the category does not exist.
        :raise CategoryNotDeletableException: If the category is not deletable.
        :return: None
        """
        await self._category_repository.delete(category_id)
