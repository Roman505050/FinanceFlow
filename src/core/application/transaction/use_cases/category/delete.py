from uuid import UUID

from core.domain.transaction.repositories.category import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: UUID) -> None:
        """Delete a operation.

        :arg category_id: The operation ID.
        :raise CategoryNotFoundException: If the operation does not exist.
        :raise CategoryNotDeletableException: If the operation
                                                is not deletable.
        :return: None
        """
        await self._category_repository.delete(category_id)
        await self._category_repository.commit()
