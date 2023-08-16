# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .model import Schema

# system imports
from datetime import date
from datetime import datetime
from datetime import timedelta

from decimal import Decimal

from typing import Any
from typing import List

from uuid import UUID

# --------------------------------------------------------------------------------------
# Serialization functions
# --------------------------------------------------------------------------------------


def sqlalchemy_array_in(value: Any) -> List[Any]:
    return value


def sqlalchemy_array_out(value: Any) -> List[Any]:
    return value


def sqlalchemy_big_integer_in(value: int) -> int:
    return value


def sqlalchemy_big_integer_out(value: int) -> int:
    return value


def sqlalchemy_boolean_in(value: bool) -> bool:
    return value


def sqlalchemy_boolean_out(value: bool) -> bool:
    return value


def sqlalchemy_date_in(value: str) -> date:
    return value


def sqlalchemy_date_out(value: date) -> str:
    return value


def sqlalchemy_date_time_in(value: str) -> datetime:
    return value


def sqlalchemy_date_time_out(value: datetime) -> int:
    return value


def sqlalchemy_double_in(value: float | Decimal) -> str:
    return value


def sqlalchemy_double_out(value: float | Decimal) -> int:
    return value


def sqlalchemy_enum_in(value: Any) -> str:
    return value


def sqlalchemy_enum_out(value: str) -> Any:
    return value


def sqlalchemy_float_in(value: float) -> str:
    return value


def sqlalchemy_float_out(value: str) -> float:
    return value


def sqlalchemy_integer_in(value: Any) -> str:
    return value


def sqlalchemy_integer_out(value: str) -> Any:
    return value


def sqlalchemy_interval_in(value: timedelta) -> str:
    return value


def sqlalchemy_interval_out(value: str) -> Any:
    return value


def sqlalchemy_large_binary_in(value: Any) -> str:
    return value


def sqlalchemy_large_binary_out(value: str) -> Any:
    return value


def sqlalchemy_json_in(value: Any) -> str:
    return value


def sqlalchemy_json_out(value: str) -> Any:
    return value


def sqlalchemy_numeric_in(value: str) -> Decimal:
    return Decimal(value)


def sqlalchemy_numeric_out(value: Decimal) -> str:
    return str(value)


def sqlalchemy_small_integer_in(value: Any) -> str:
    return value


def sqlalchemy_small_integer_out(value: str) -> Any:
    return value


def sqlalchemy_string_in(value: str) -> str:
    return value


def sqlalchemy_string_out(value: str) -> str:
    return value


def sqlalchemy_text_in(value: Any) -> str:
    return value


def sqlalchemy_text_out(value: str) -> Any:
    return value


def sqlalchemy_time_in(value: Any) -> str:
    return value


def sqlalchemy_time_out(value: str) -> Any:
    return value


def sqlalchemy_unicode_in(value: Any) -> str:
    return value


def sqlalchemy_unicode_out(value: str) -> Any:
    return value


def sqlalchemy_unicode_text_in(value: Any) -> str:
    return value


def sqlalchemy_unicode_text_out(value: str) -> Any:
    return value


def sqlalchemy_uuid_in(value: str) -> UUID:
    return UUID(value)


def sqlalchemy_uuid_out(value: UUID) -> str:
    return str(value)


# --------------------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------------------


class JsonSchema(Schema):
    def from_message(self, message: Any) -> Any:
        """
        Returns a deserialized model.

        Parameters:
            message (object): Message.
        """
        print(">>> JsonSchema.from_message()")

    def to_message(self, model: Any) -> Any:
        """
        Returns a serialized model.

        Parameters:
            model (object): Model.
        """
        print(">>> JsonSchema.to_message()")
