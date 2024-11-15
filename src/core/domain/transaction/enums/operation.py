from enum import Enum
from typing import Literal, Dict


class OperationType(Enum):
    INCOME = 0
    EXPENSE = 1
    INVESTMENT = 2


def get_operation_type_string(
    operation_type: OperationType,
) -> Literal["income", "expense", "investment"]:
    mapping: dict[
        OperationType, Literal["income", "expense", "investment"]
    ] = {
        OperationType.INCOME: "income",
        OperationType.EXPENSE: "expense",
        OperationType.INVESTMENT: "investment",
    }
    return mapping[operation_type]


def get_operation_type_enum(
    operation_type: Literal["income", "expense", "investment"],
) -> OperationType:
    mapping: Dict[
        Literal["income", "expense", "investment"], OperationType
    ] = {
        "income": OperationType.INCOME,
        "expense": OperationType.EXPENSE,
        "investment": OperationType.INVESTMENT,
    }
    return mapping[operation_type]
