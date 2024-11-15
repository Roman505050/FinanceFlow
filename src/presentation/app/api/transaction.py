from flask import Blueprint, request, jsonify, session
from pydantic import ValidationError
from loguru import logger
from uuid import UUID

from core.application.transaction.dto.transaction import CreateTransactionDTO
from core.application.transaction.use_cases.transaction.create import (
    CreateTransactionUseCase,
)
from core.application.transaction.use_cases.transaction.delete import (
    DeleteTransactionUseCase,
)
from core.application.transaction.use_cases.transaction.get_all_by_user import (  # noqa: E501
    GetAllTransactionsByUserUseCase,
)
from core.domain.transaction.exceptions.category.not_found import (
    CategoryNotFoundException,
)
from core.domain.transaction.exceptions.currency.not_found import (
    CurrencyNotFoundException,
)
from core.domain.transaction.exceptions.transaction.not_found import (
    TransactionNotFoundException,
)
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.category import CategoryRepository
from core.infrastructure.repositories.currency import CurrencyRepository
from core.infrastructure.repositories.transaction import TransactionRepository
from core.shared.exceptions import ForbiddenException
from presentation.app.utils.permissions import has_permissions
from presentation.app.utils.tools import get_current_user, get_parsed_errors

transaction_api_bp = Blueprint("transaction_api", __name__)


@transaction_api_bp.route("", methods=["POST"])
async def create_transaction():
    """
    Create a transaction.
    ---
    tags:
        - Transactions
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            category_id:
              type: string
              format: uuid
              example: "123e4567-e89b-12d3-a456-426614174000"
            currency_id:
                type: string
                format: uuid
                example: "123e4567-e89b-12d3-a456-426614174000"
            amount:
                type: number
                example: 10.0
            date:
                type: string
                format: date-time
                example: "2021-10-10T10:00:00+00:00"
            description:
                type: string
                example: "This is a description"
    responses:
      201:
        description: Transaction created
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            transaction:
              type: object
              properties:
                transaction_id:
                  type: string
                  format: uuid
                  example: "123e4567-e89b-12d3-a456-426614174000"
                user_id:
                  type: string
                  format: uuid
                  example: "123e4567-e89b-12d3-a456-426614174000"
                  category_id: UUID
                category_name:
                  type: string
                  example: "Category name"
                operation_id:
                  type: string
                  format: uuid
                  example: "123e4567-ed9b-12d3-a456-426614174000"
                operation_name:
                  type: string
                  example: "Operation name"
                operation_type:
                  type: string
                  example: "income"
                currency_id:
                  type: string
                  format: uuid
                  example: "123e4567-e39b-12d3-a456-426614174000"
                currency_name:
                  type: string
                  example: "Currency name"
                currency_code:
                  type: string
                  example: "USD"
                currency_symbol:
                  type: string
                  example: "$"
                amount:
                  type: string
                  example: "10.0"
                description:
                  type: string
                  example: "This is a description"
                date:
                  type: string
                  format: date-time
                  example: "2021-10-10T10:00:00+00:00"
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
                  example: "Category not found"
      404.1:
        description: Currency not found
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
                  example: "CURRENCY_NOT_FOUND"
                message:
                  type: string
                  example: "Currency not found"
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
      422:
        description: Invalid body
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
                  example: "Invalid body"
                errors:
                  type: object
                  example: {
                              "category_id": ["Field required"],
                              "amount": ["Amount must be greater than 0"],
                              "description": ["Description must be at least
                              10 characters long"],
                              "date": ["Invalid date format"],
                              "currency_id": ["Field required"]
                            }
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
        if not has_permissions(user, ["member"]):
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
            create_transaction_dto = CreateTransactionDTO(
                user_id=user.user_id, **body
            )
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": "INVALID_BODY",
                        "errors": get_parsed_errors(e),
                    }
                ),
                422,
            )

        async with SessionContextManager() as db_session:
            transaction_repository = TransactionRepository(db_session)
            category_repository = CategoryRepository(db_session)
            currency_repository = CurrencyRepository(db_session)
            use_case = CreateTransactionUseCase(
                transaction_repository,
                category_repository,
                currency_repository,
            )
            try:
                transaction = await use_case.execute(create_transaction_dto)
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
            except CurrencyNotFoundException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "CURRENCY_NOT_FOUND",
                                "message": str(e),
                            },
                        }
                    ),
                    404,
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
        jsonify(
            {"ok": True, "transaction": transaction.model_dump(mode="json")}
        ),
        201,
    )


@transaction_api_bp.route("/me", methods=["GET"])
async def get_user_transactions():
    """
    Get user transactions.
    ---
    tags:
        - Transactions
    responses:
      200:
        description: Transaction created
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            transactions:
              type: array
              items:
                type: object
                properties:
                  transaction_id:
                    type: string
                    format: uuid
                    example: "123e4567-e89b-12d3-a456-426614174000"
                  user_id:
                    type: string
                    format: uuid
                    example: "123e4567-e89b-12d3-a456-426614174000"
                    category_id: UUID
                  category_name:
                    type: string
                    example: "Category name"
                  operation_id:
                    type: string
                    format: uuid
                    example: "123e4567-ed9b-12d3-a456-426614174000"
                  operation_name:
                    type: string
                    example: "Operation name"
                  operation_is_income:
                    type: boolean
                    example: true
                  currency_id:
                    type: string
                    format: uuid
                    example: "123e4567-e39b-12d3-a456-426614174000"
                  currency_name:
                    type: string
                    example: "Currency name"
                  currency_code:
                    type: string
                    example: "USD"
                  currency_symbol:
                    type: string
                    example: "$"
                  amount:
                    type: string
                    example: "10.0"
                  description:
                    type: string
                    example: "This is a description"
                  date:
                    type: string
                    format: date-time
                    example: "2021-10-10T10:00:00+00:00"
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
        if not has_permissions(user, ["member"]):
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
            transaction_repository = TransactionRepository(db_session)
            use_case = GetAllTransactionsByUserUseCase(transaction_repository)
            transactions = await use_case.execute(user.user_id)
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
                "transactions": [
                    transaction.model_dump(mode="json")
                    for transaction in transactions
                ],
            }
        ),
        200,
    )


@transaction_api_bp.route("/<uuid:transaction_id>", methods=["DELETE"])
async def delete_transaction(transaction_id: UUID):
    """
    Delete a transaction.
    ---
    tags:
        - Transactions
    parameters:
      - in: path
        name: transaction_id
        schema:
          type: uuid
          example: "00000000-0000-0000-0000-000000000000"
    responses:
      200:
        description: Transaction deleted
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
      404:
        description: Transaction not found
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
                   example: "TRANSACTION_NOT_FOUND"
                 message:
                   type: string
                   example: "Transaction not found"
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
      403.1:
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
                  example: "You are not allowed to delete this transaction"
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
        if not has_permissions(user, ["member"]):
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
            transaction_repository = TransactionRepository(db_session)
            use_case = DeleteTransactionUseCase(transaction_repository)
            try:
                await use_case.execute(
                    user_id=user.user_id, transaction_id=transaction_id
                )
            except ForbiddenException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "FORBIDDEN",
                                "message": str(e),
                            },
                        }
                    ),
                    403,
                )
            except TransactionNotFoundException as e:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {
                                "type": "TRANSACTION_NOT_FOUND",
                                "message": str(e),
                            },
                        }
                    ),
                    404,
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
