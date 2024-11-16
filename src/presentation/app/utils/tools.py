from flask.sessions import SessionMixin
from pydantic import ValidationError
from loguru import logger
import json

from core.application.user.dto.user import UserDTO
from core.application.user.use_cases.get_user import GetUserUseCase
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.user import UserRepository


def get_parsed_errors(error: ValidationError) -> dict:
    parsed_errors = {}
    errors: list[dict] = json.loads(error.json())

    for err in errors:
        try:
            parsed_errors[err["loc"][0]] = err.get("msg")
        except KeyError as e:
            logger.error(f"Error parsing error: {e}")
            parsed_errors["unknown"] = err.get("msg")

    return parsed_errors


async def get_current_user(session: SessionMixin) -> UserDTO | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None
    async with SessionContextManager() as db_session:
        user_repository = UserRepository(db_session)
        use_case = GetUserUseCase(user_repository)
        user = await use_case.execute(user_id)
        return user
