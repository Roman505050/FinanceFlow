from flask import Blueprint, request, jsonify, session
from pydantic import ValidationError
from loguru import logger
from uuid import UUID

from core.application.transaction.dto.operation import (
    CreateOperationDTO,
)
from core.application.transaction.use_cases.operation.create import (
    CreateOperationUseCase,
)
from core.application.transaction.use_cases.operation.delete import (
    DeleteOperationUseCase,
)
from core.application.transaction.use_cases.operation.get_all import (
    GetAllOperationUseCase,
)
from core.domain.transaction.exceptions.operation.already_exist import (
    OperationAlreadyExistException,
)
from core.domain.transaction.exceptions.operation.delete import (
    OperationNotDeletableException,
)
from core.domain.transaction.exceptions.operation.not_found import (
    OperationNotFoundException,
)
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.operation import OperationRepository
from presentation.app.utils.permissions import has_permissions
from presentation.app.utils.tools import get_parsed_errors, get_current_user

operation_api_bp = Blueprint("operation_api", __name__)


@operation_api_bp.route("/operation", methods=["POST"])
async def create_operation():
    """
    Create a new operation
    ---
    tags:
      - Operations
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            operation_name:
              type: string
              example: "Operation Name"
    responses:
      201:
        description: Operation created
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            operation:
              type: object
              properties:
                operation_name:
                  type: string
                  example: "Operation Name"
      400:
        description: Invalid body
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            message:
              type: string
              example: "INVALID_BODY"
            errors:
              type: object
              example:
                operation_name:
                  - "Missing data for required field."
    """
    try:
        user = await get_current_user(session)
        if user is None:
            return jsonify({"ok": False, "message": "UNAUTHORIZED"}), 401
        if not has_permissions(user, ["admin"]):
            return jsonify({"ok": False, "message": "FORBIDDEN"}), 403

        body = request.get_json()
        try:
            operation = CreateOperationDTO(**body)
        except ValidationError as error:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": "INVALID_BODY",
                        "errors": get_parsed_errors(error),
                    }
                ),
                400,
            )

        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = CreateOperationUseCase(operation_repository)
            try:
                operation = await use_case.execute(operation)
            except OperationAlreadyExistException as error:
                return (
                    jsonify({"ok": False, "message": str(error)}),
                    400,
                )
    except Exception as error:
        logger.error(error)
        return jsonify({"ok": False, "message": "INTERNAL_SERVER_ERROR"}), 500

    return jsonify({"ok": True, "operation": operation.model_dump()}), 201


@operation_api_bp.route("/operation/<uuid:operation_id>", methods=["DELETE"])
async def delete_operation(operation_id: UUID):
    """
    Delete an operation
    ---
    tags:
      - Operations
    parameters:
      - in: path
        name: operation_id
        schema:
          type: uuid
          example: "00000000-0000-0000-0000-000000000000"

    responses:
        200:
            description: Operation deleted
            schema:
                type: object
                properties:
                    ok:
                        type: boolean
                        example: true
        400:
            description: Operation not found
            schema:
                type: object
                properties:
                    ok:
                        type: boolean
                        example: false
                    message:
                        type: string
                        example: "Operation not found"
        401:
            description: Unauthorized
            schema:
                type: object
                properties:
                    ok:
                        type: boolean
                        example: false
                    message:
                        type: string
                        example: "UNAUTHORIZED"
        403:
            description: Forbidden
            schema:
                type: object
                properties:
                    ok:
                        type: boolean
                        example: false
                    message:
                        type: string
                        example: "FORBIDDEN"
    """
    try:
        user = await get_current_user(session)
        if user is None:
            return jsonify({"ok": False, "message": "UNAUTHORIZED"}), 401
        if not has_permissions(user, ["admin"]):
            return jsonify({"ok": False, "message": "FORBIDDEN"}), 403

        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = DeleteOperationUseCase(operation_repository)
            try:
                await use_case.execute(operation_id)
            except OperationNotFoundException as error:
                return (
                    jsonify({"ok": False, "message": str(error)}),
                    400,
                )
            except OperationNotDeletableException as error:
                return (
                    jsonify({"ok": False, "message": str(error)}),
                    400,
                )
    except Exception as error:
        logger.error(error)
        return jsonify({"ok": False, "message": "INTERNAL_SERVER_ERROR"}), 500

    return jsonify({"ok": True}), 200


@operation_api_bp.route("/operation", methods=["GET"])
async def get_all_operations():
    """
    Get all operations
    ---
    tags:
      - Operations
    responses:
      200:
        description: Operations list
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            operations:
              type: array
              items:
                type: object
                properties:
                  operation_id:
                    type: string
                    example: "00000000-0000-0000-0000-000000000000"
                  operation_name:
                    type: string
                    example: "Operation Name"
    """
    try:
        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = GetAllOperationUseCase(operation_repository)
            operations = await use_case.execute()
    except Exception as error:
        logger.error(error)
        return jsonify({"ok": False, "message": "INTERNAL_SERVER_ERROR"}), 500

    return (
        jsonify(
            {
                "ok": True,
                "operations": [
                    operation.model_dump() for operation in operations
                ],
            }
        ),
        200,
    )


@operation_api_bp.route("/autocomplete/operation", methods=["GET"])
async def autocomplete_operation():
    """
    Autocomplete operations
    ---
    tags:
      - Operations
    responses:
      200:
        description: Operations list
        schema:
          type: array
          items:
            type: object
            properties:
              label:
                type: string
                example: "Operation Name"
              value:
                type: string
                example: "00000000-0000-0000-0000-000000000000"
    """
    try:
        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = GetAllOperationUseCase(operation_repository)
            operations = await use_case.execute()
    except Exception as error:
        logger.error(error)
        return jsonify({"ok": False, "message": "INTERNAL_SERVER_ERROR"}), 500

    return (
        jsonify(
            [
                {
                    "label": operation.operation_name,
                    "value": str(operation.operation_id),
                }
                for operation in operations
            ]
        ),
        200,
    )
