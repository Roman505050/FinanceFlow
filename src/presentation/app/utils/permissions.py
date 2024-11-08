from core.application.user.dto.user import UserDTO


def has_permissions(user: UserDTO, needed_roles: list[str]) -> bool:
    user_roles = [role.role_name for role in user.roles]
    return any(role in user_roles for role in needed_roles)
