from uuid import UUID

from flask import Blueprint, jsonify, request, session
from loguru import logger
from pydantic import ValidationError

from core.application.transaction.dto.category import CreateCategoryDTO
from core.application.transaction.use_cases.category.create import (
    CreateCategoryUseCase,
)
from core.application.transaction.use_cases.category.delete import (
    DeleteCategoryUseCase,
)
from core.application.transaction.use_cases.category.get_all import (
    GetAllCategoriesUseCase,
)
from core.application.transaction.use_cases.category.get_all_by_operation import (  # noqa: E501
    GetAllCategoriesByOperationUseCase,
)
from core.domain.transaction.exceptions.category.already_exist import (
    CategoryAlreadyExistException,
)
from core.domain.transaction.exceptions.category.delete import (
    CategoryNotDeletableException,
)
from core.domain.transaction.exceptions.category.not_found import (
    CategoryNotFoundException,
)
from core.domain.transaction.exceptions.operation.not_found import (
    OperationNotFoundException,
)
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.category import CategoryRepository
from core.infrastructure.repositories.operation import OperationRepository
from presentation.app.utils.permissions import has_permissions
from presentation.app.utils.tools import get_current_user, get_parsed_errors


category_api_bp = Blueprint("category_api", __name__)


@category_api_bp.route("", methods=["POST"])
async def create_category():
    """
    Create a new category
    ---
    tags:
      - Categories
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            category_name:
              type: string
              example: "Category Name"
            operation_id:
              type: string
              example: "00000000-0000-0000-0000-000000000000"
    responses:
      201:
        description: Category created
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            category:
              type: object
              properties:
                category_id:
                  type: string
                  example: "00000000-0000-0000-0000-000000000000"
                category_name:
                  type: string
                  example: "Category Name"
                operation_name:
                  type: string
                  example: "Operation Name"
      422:
        description: Unprocessable Entity (Invalid body)
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
                  example: "INVALID_BODY"
                message:
                  type: string
                  example: "The request body is invalid"
                errors:
                  type: object
                  example:
                    category_name:
                      - "Missing data for required field."
                    operation_id:
                      - "Missing data for required field."
      400:
        description: Bad Request (Category already exists)
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
                  example: "CATEGORY_ALREADY_EXISTS"
                message:
                  type: string
                  example: "Category with name {category_name} already
                            exists for operation {operation_name}"
      404:
        description: Not Found (Operation not found)
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
                  example: "Operation with id {operation_id} not found"
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
            create_category_dto = CreateCategoryDTO(**body)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": {
                            "type": "INVALID_BODY",
                            "message": "The request body is invalid",
                            "errors": get_parsed_errors(e),
                        },
                    }
                ),
                422,
            )

        async with SessionContextManager() as db_session:
            category_repository = CategoryRepository(db_session)
            operation_repository = OperationRepository(db_session)
            use_case = CreateCategoryUseCase(
                category_repository, operation_repository
            )
            try:
                category = await use_case.execute(create_category_dto)
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
                    404,
                )
            except CategoryAlreadyExistException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "CATEGORY_ALREADY_EXISTS",
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

    return jsonify({"ok": True, "category": category.model_dump()}), 201


@category_api_bp.route("", methods=["GET"])
async def get_all_categories():
    """
    Get all categories
    ---
    tags:
      - Categories
    responses:
      200:
        description: Categories list
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            categories:
              type: array
              items:
                type: object
                properties:
                  category_id:
                    type: string
                    example: "00000000-0000-0000-0000-000000000000"
                  category_name:
                    type: string
                    example: "Category Name"
                  operation_name:
                    type: string
                    example: "Operation Name"
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
            category_repository = CategoryRepository(db_session)
            use_case = GetAllCategoriesUseCase(category_repository)
            categories = await use_case.execute()
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
                "categories": [
                    category.model_dump() for category in categories
                ],
            }
        ),
        200,
    )


@category_api_bp.route("/autocomplete", methods=["GET"])
async def autocomplete_category():
    """
    Autocomplete categories
    ---
    tags:
      - Categories
      - Autocomplete
    parameters:
      - in: query
        name: operation_id
        required: false
        schema:
          type: string
          format: uuid
          example: "00000000-0000-0000-0000-000000000000"
    responses:
      200:
        description: Categories list
        schema:
          type: object
          properties:
            label:
              type: string
              example: "Category Name"
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
        query = request.args.to_dict()
        try:
            operation_id: UUID | None = (
                UUID(query["operation_id"])
                if query.get("operation_id")
                else None
            )
        except ValueError:
            operation_id = None

        async with SessionContextManager() as db_session:
            category_repository = CategoryRepository(db_session)
            if operation_id is None:
                use_case = GetAllCategoriesUseCase(category_repository)
                categories = await use_case.execute()
            else:
                use_case_by_operation = GetAllCategoriesByOperationUseCase(
                    category_repository
                )
                categories = await use_case_by_operation.execute(operation_id)

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
                    "label": category.category_name,
                    "value": str(category.category_id),
                }
                for category in categories
            ]
        ),
        200,
    )


@category_api_bp.route("/<uuid:operation_id>", methods=["DELETE"])
async def delete_category(operation_id: UUID):
    """
    Delete a category
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: operation_id
        required: true
        schema:
          type: string
          format: uuid
          example: "00000000-0000-0000-0000-000000000000"
    responses:
      200:
        description: Category deleted
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
      404:
        description: Category not found
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
                example: "CATEGORY_NOT_FOUND"
              message:
                type: string
                example: "Category with id {category_id} not found"
      400:
        description: Bad Request (Category not deletable)
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
                example: "CATEGORY_NOT_DELETABLE"
              message:
                type: string
                example: "Category with id {category_id} not deletable"
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
            category_repository = CategoryRepository(db_session)
            use_case = DeleteCategoryUseCase(category_repository)
            try:
                await use_case.execute(operation_id)
            except CategoryNotFoundException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "CATEGORY_NOT_FOUND",
                                "message": str(e),
                            },
                        }
                    ),
                    404,
                )
            except CategoryNotDeletableException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "CATEGORY_NOT_DELETABLE",
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
