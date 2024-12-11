from uuid import UUID

from flask import Blueprint, jsonify, request, session
from loguru import logger
from pydantic import ValidationError

from core.application.transaction.dto.currency import CreateCurrencyDTO
from core.application.transaction.use_cases.currency.create import (
    CreateCurrencyUseCase,
)
from core.application.transaction.use_cases.currency.delete import (
    DeleteCurrencyUseCase,
)
from core.application.transaction.use_cases.currency.get_all import (
    GetAllCurrencyUseCase,
)
from core.domain.transaction.exceptions.currency.already_exist import (
    CurrencyAlreadyExistException,
)
from core.domain.transaction.exceptions.currency.delete import (
    CurrencyNotDeletableException,
)
from core.domain.transaction.exceptions.currency.not_found import (
    CurrencyNotFoundException,
)
from core.infrastructure.database.core import SessionContextManager
from core.infrastructure.repositories.currency import CurrencyRepository
from presentation.app.utils.permissions import has_permissions
from presentation.app.utils.tools import get_current_user, get_parsed_errors


currency_api_bp = Blueprint("currency_api", __name__)


@currency_api_bp.route("", methods=["POST"])
async def create_currency():
    """
    Create a new currency
    ---
    tags:
      - Currencies
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            currency_code:
              type: string
              example: "USD"
            currency_name:
              type: string
              example: "US Dollar"
            currency_symbol:
              type: string
              example: "$"
    responses:
      201:
        description: Currency created
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            currency:
              type: object
              properties:
                currency_id:
                  type: string
                  example: "00000000-0000-0000-0000-000000000000"
                currency_code:
                  type: string
                  example: "USD"
                currency_name:
                  type: string
                  example: "US Dollar"
                currency_symbol:
                  type: string
                  example: "$"
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
                    currency_code:
                      - "Missing data for required field."
                    currency_name:
                      - "Missing data for required field."
                    currency_symbol:
                        - "Missing data for required field."
      400:
        description: Bad Request (Currency already exists)
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
                  example: "CURRENCY_ALREADY_EXISTS"
                message:
                  type: string
                  example: "Currency with code {currency_code} already exists"
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
            create_currency_dto = CreateCurrencyDTO(**body)
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
            category_repository = CurrencyRepository(db_session)
            use_case = CreateCurrencyUseCase(category_repository)
            try:
                currency = await use_case.execute(create_currency_dto)
            except CurrencyAlreadyExistException as e:
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

    return jsonify({"ok": True, "currency": currency.model_dump()}), 201


@currency_api_bp.route("", methods=["GET"])
async def get_currency():
    """
    Get all currencies
    ---
    tags:
      - Currencies
    responses:
      200:
        description: Currencies found
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
            currencies:
              type: array
              items:
                type: object
                properties:
                  currency_id:
                    type: string
                    example: "00000000-0000-0000-0000-000000000000"
                  currency_code:
                    type: string
                    example: "USD"
                  currency_name:
                    type: string
                    example: "US Dollar"
                  currency_symbol:
                    type: string
                    example: "$"
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
            category_repository = CurrencyRepository(db_session)
            use_case = GetAllCurrencyUseCase(category_repository)
            currencies = await use_case.execute()
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
                "currencies": [
                    currency.model_dump() for currency in currencies
                ],
            }
        ),
        200,
    )


@currency_api_bp.route("/autocomplete", methods=["GET"])
async def autocomplete_currency():
    """
    Autocomplete categories
    ---
    tags:
      - Currencies
      - Autocomplete
    responses:
      200:
        description: Categories list
        schema:
          type: object
          properties:
            label:
              type: string
              example: "USD $"
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
            category_repository = CurrencyRepository(db_session)
            use_case = GetAllCurrencyUseCase(category_repository)
            currencies = await use_case.execute()
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
                    "label": (
                        f"{currency.currency_code} "
                        f"{currency.currency_symbol}"
                    ),
                    "value": str(currency.currency_id),
                }
                for currency in currencies
            ]
        ),
        200,
    )


@currency_api_bp.route("/<uuid:currency_id>", methods=["DELETE"])
async def delete_currency(currency_id: UUID):
    """
    Delete a currency
    ---
    tags:
      - Currencies
    parameters:
      - in: path
        name: currency_id
        required: true
        schema:
        type: string
        format: uuid
        example: "00000000-0000-0000-0000-000000000000"
    responses:
      200:
        description: Currency deleted
        schema:
          type: object
          properties:
            ok:
              type: boolean
              example: true
      404:
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
                example: "Currency with id {currency_id} not found"
      400:
        description: Bad Request (Currency not deletable)
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
                example: "CURRENCY_NOT_DELETABLE"
              message:
                type: string
                example: "Currency with id {currency_id} is not deletable"
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
            category_repository = CurrencyRepository(db_session)
            use_case = DeleteCurrencyUseCase(category_repository)
            try:
                await use_case.execute(currency_id)
            except CurrencyNotFoundException as e:
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
            except CurrencyNotDeletableException as e:
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
