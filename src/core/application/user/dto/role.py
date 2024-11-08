from pydantic import BaseModel
from uuid import UUID

from core.domain.user.entities.role import RoleEntity


class RoleDTO(BaseModel):
    role_id: UUID
    role_name: str

    @staticmethod
    def from_entity(entity: RoleEntity) -> "RoleDTO":
        return RoleDTO(
            role_id=entity.role_id,
            role_name=entity.role_name,
        )
