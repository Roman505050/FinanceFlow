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


@operation_api_bp.route("", methods=["POST"])
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
              operation_type:
                type: string
                example: "income | expense | investment"
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
                operation_type:
                  type: string
                  example: "income"
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
                is_income:
                  - "Missing data for required field."
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "UNAUTHORIZED"
                message:
                  type: string
                  example: "Missing authentication token"
      403:
        description: Forbidden
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "FORBIDDEN"
                message:
                  type: string
                  example: "You don't have permission to access this resource"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "INTERNAL_ERROR"
                message:
                  type: string
                  example: "Something went wrong"
    """
    try:
        user = await get_current_user(session)
        if user is None:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "UNAUTHORIZED",
                            "message": "Missing authentication token",
                        },
                    }
                ),
                401,
            )
        if not has_permissions(user, ["admin"]):
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "FORBIDDEN",
                            "message": (
                                "You don't have permission "
                                "to access this resource"
                            ),
                        },
                    }
                ),
                403,
            )

        body = request.get_json()
        try:
            operation = CreateOperationDTO(**body)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "INVALID_BODY",
                            "message": "Invalid body",
                            "errors": get_parsed_errors(e),
                        },
                    }
                ),
                400,
            )

        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = CreateOperationUseCase(operation_repository)
            try:
                operation = await use_case.execute(operation)
            except OperationAlreadyExistException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "ALREADY_EXIST",
                                "message": str(e),
                            },
                        }
                    ),
                    400,
                )
    except Exception as e:
        logger.error(e)
        return (
            jsonify(
                {
                    "ok": False,
                    "error": {
                        "type": "INTERNAL_ERROR",
                        "message": "Something went wrong",
                    },
                }
            ),
            500,
        )

    return (
        jsonify({"ok": True, "operation": operation.model_dump(mode="json")}),
        201,
    )


@operation_api_bp.route("/<uuid:operation_id>", methods=["DELETE"])
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
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "OPERATION_NOT_FOUND"
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
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "UNAUTHORIZED"
                message:
                  type: string
                  example: "Missing authentication token"
      403:
        description: Forbidden
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "FORBIDDEN"
                message:
                  type: string
                  example: "You don't have permission to access this resource"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "INTERNAL_ERROR"
                message:
                  type: string
                  example: "Something went wrong"
    """
    try:
        user = await get_current_user(session)
        if user is None:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "UNAUTHORIZED",
                            "message": "Missing authentication token",
                        },
                    }
                ),
                401,
            )
        if not has_permissions(user, ["admin"]):
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "FORBIDDEN",
                            "message": (
                                "You don't have permission "
                                "to access this resource"
                            ),
                        },
                    }
                ),
                403,
            )

        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = DeleteOperationUseCase(operation_repository)
            try:
                await use_case.execute(operation_id)
            except OperationNotFoundException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "OPERATION_NOT_FOUND",
                                "message": str(e),
                            },
                        }
                    ),
                    400,
                )
            except OperationNotDeletableException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "OPERATION_NOT_DELETABLE",
                                "message": str(e),
                            },
                        }
                    ),
                    400,
                )
    except Exception as e:
        logger.error(e)
        return (
            jsonify(
                {
                    "ok": False,
                    "error": {
                        "type": "INTERNAL_ERROR",
                        "message": "Something went wrong",
                    },
                }
            ),
            500,
        )

    return jsonify({"ok": True}), 200


@operation_api_bp.route("", methods=["GET"])
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
                  operation_type:
                    type: string
                    example: "income"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "INTERNAL_ERROR"
                message:
                  type: string
                  example: "Something went wrong"
    """
    try:
        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = GetAllOperationUseCase(operation_repository)
            operations = await use_case.execute()
    except Exception as e:
        logger.error(e)
        return (
            jsonify(
                {
                    "ok": False,
                    "error": {
                        "type": "INTERNAL_ERROR",
                        "message": "Something went wrong",
                    },
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "ok": True,
                "operations": [
                    operation.model_dump(mode="json")
                    for operation in operations
                ],
            }
        ),
        200,
    )


@operation_api_bp.route("/autocomplete", methods=["GET"])
async def autocomplete_operation():
    """
    Autocomplete operations
    ---
    tags:
      - Operations
      - Autocomplete
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
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: false
            error:
              type: object
              properties:
                type:
                  type: string
                  example: "INTERNAL_ERROR"
                message:
                  type: string
                  example: "Something went wrong"
    """
    try:
        async with SessionContextManager() as db_session:
            operation_repository = OperationRepository(db_session)
            use_case = GetAllOperationUseCase(operation_repository)
            operations = await use_case.execute()
    except Exception as e:
        logger.error(e)
        return (
            jsonify(
                {
                    "ok": False,
                    "error": {
                        "type": "INTERNAL_ERROR",
                        "message": "Something went wrong",
                    },
                }
            ),
            500,
        )

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
