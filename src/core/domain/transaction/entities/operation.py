from dataclasses import dataclass
from uuid import UUID


@dataclass
class OperationEntity:
    operation_id: UUID
    operation_name: str
