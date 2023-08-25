# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import Field

from . import NumericParams

# system imports
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

from decimal import Decimal

from typing import Any
from typing import List
from typing import Optional
from typing import Union
from typing import cast

from uuid import UUID

# dependency imports
from sqlalchemy import Column


def array_from_json(field: Field, value: Optional[List[Any]]) -> Optional[List[Any]]:
    return value


def array_params(column: Column) -> Any:
    return


def array_to_json(field: Field, value: Optional[List[Any]]) -> Optional[List[Any]]:
    return value


def biginteger_from_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def biginteger_params(column: Column) -> Any:
    return


def biginteger_to_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def boolean_from_json(field: Field, value: Optional[bool]) -> Optional[bool]:
    return value


def boolean_params(column: Column) -> Any:
    return


def boolean_to_json(field: Field, value: Optional[bool]) -> Optional[bool]:
    return value


def date_from_json(field: Field, value: Optional[str]) -> Optional[date]:
    if value is None:
        return None

    return date.fromisoformat(value)


def date_params(column: Column) -> Any:
    return


def date_to_json(field: Field, value: Optional[date]) -> Optional[date]:
    return value


def datetime_from_json(field: Field, value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None

    return datetime.fromisoformat(value)


def datetime_params(column: Column) -> Any:
    return


def datetime_to_json(field: Field, value: Optional[datetime]) -> Optional[datetime]:
    return value


def double_from_json(
    field: Field[NumericParams], value: Optional[Union[float, str]]
) -> Optional[Union[Decimal, float]]:
    return numeric_from_json(field, value)


def double_params(column: Column) -> NumericParams:
    return NumericParams(
        cast(Any, column.type).precision,
        None,
        cast(Any, column.type).decimal_return_scale,
        cast(Any, column.type).asdecimal,
    )


def double_to_json(
    field: Field[NumericParams], value: Optional[Union[Decimal, float]]
) -> Optional[Union[float, str]]:
    return numeric_to_json(field, value)


def enum_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def enum_params(column: Column) -> Any:
    return


def enum_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def float_from_json(
    field: Field[NumericParams], value: Optional[Union[float, str]]
) -> Optional[Union[Decimal, float]]:
    return numeric_from_json(field, value)


def float_params(column: Column) -> NumericParams:
    return NumericParams(
        cast(Any, column.type).precision,
        None,
        cast(Any, column.type).decimal_return_scale,
        cast(Any, column.type).asdecimal,
    )


def float_to_json(
    field: Field[NumericParams], value: Optional[Union[Decimal, float]]
) -> Optional[Union[float, str]]:
    return numeric_to_json(field, value)


def integer_from_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def integer_params(column: Column) -> Any:
    return


def integer_to_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def interval_from_json(field: Field, value: Optional[List[int]]) -> Optional[timedelta]:
    if value is None:
        return None

    return timedelta(hours=value[0], seconds=value[1], microseconds=value[2])


def interval_params(column: Column) -> Any:
    return


def interval_to_json(field: Field, value: Optional[timedelta]) -> Optional[List[int]]:
    if value is None:
        return None

    return [value.days, value.seconds, value.microseconds]


def largebinary_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def largebinary_params(column: Column) -> Any:
    return


def largebinary_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def json_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def json_params(column: Column) -> Any:
    return


def json_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def numeric_from_json(
    field: Field[NumericParams], value: Optional[Union[float, str]]
) -> Optional[Union[Decimal, float]]:
    if value is None:
        return None

    elif field.params.asdecimal:
        return Decimal(value)

    else:
        return cast(float, value)


def numeric_params(column: Column) -> NumericParams:
    return NumericParams(
        cast(Any, column.type).precision,
        cast(Any, column.type).scale,
        cast(Any, column.type).decimal_return_scale,
        cast(Any, column.type).asdecimal,
    )


def numeric_to_json(
    field: Field[NumericParams], value: Optional[Union[Decimal, float]]
) -> Optional[Union[float, str]]:
    if value is None:
        return None

    elif field.params.asdecimal:
        return str(round(value, field.params.scale))

    else:
        return cast(float, value)


def smallinteger_from_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def smallinteger_params(column: Column) -> Any:
    return


def smallinteger_to_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def string_from_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def string_params(column: Column) -> Any:
    return


def string_to_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def text_from_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def text_params(column: Column) -> Any:
    return


def text_to_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def time_from_json(field: Field, value: Optional[str]) -> Optional[time]:
    if value is None:
        return None

    return time.fromisoformat(value)


def time_params(column: Column) -> Any:
    return


def time_to_json(field: Field, value: Optional[time]) -> Optional[time]:
    return value


def unicode_from_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def unicode_params(column: Column) -> Any:
    return


def unicode_to_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def unicodetext_from_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def unicodetext_params(column: Column) -> Any:
    return


def unicodetext_to_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def uuid_from_json(field: Field, value: Optional[str]) -> Optional[UUID]:
    if value is None:
        return None

    return UUID(value)


def uuid_params(column: Column) -> Any:
    return


def uuid_to_json(field: Field, value: Optional[UUID]) -> Optional[UUID]:
    return value
