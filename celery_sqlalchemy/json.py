# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .model import schema_for_model
from .model import schema_for_model_path
from .model import schema_map_key

from .schema import Field

# system imports
from collections import namedtuple

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

from decimal import Decimal

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from typing import cast

from uuid import UUID

import sys

# dependency imports
from celery import Celery

from kombu import serialization

from sqlalchemy.exc import NoInspectionAvailable

from sqlalchemy import Column
from sqlalchemy import inspect

import orjson

json_module_key = "$model_path$"
orjson_opts = 0


def arg_from_json(arg: Any) -> Any:
    """
    Deserialize a single task argument into its python equivalent.

    Parameters:
        arg (object): Any object type.
    """
    if isinstance(arg, dict) and json_module_key in arg:
        schema = schema_for_model_path(arg[json_module_key], sys.modules[__name__])

        return schema.model(
            **{
                field.name: field.from_json(field, arg.get(field.name))
                for field in schema.fields
            }
        )

    else:
        return arg


def arg_to_json(arg: Any) -> Any:
    """
    Serialize a single task argument into its JSON equivalent.

    Parameters:
        arg (object): Any object type.
    """
    if hasattr(arg, "__table__"):
        try:
            instance_state = inspect(arg)
            mapper = instance_state.mapper
            schema = schema_for_model(arg, mapper, sys.modules[__name__])

            json = {
                field.name: field.to_json(field, getattr(arg, field.name))
                for field in schema.fields
            }

            json[json_module_key] = schema_map_key(arg)

            return json

        except NoInspectionAvailable:
            return arg

    else:
        return arg


def initialize(
    celery: Celery,
    json_key: str = "$model_path$",
    naive_utc: bool = True,
    utc_z: bool = False,
) -> None:
    """
    Initialize the JSON module.

    Parameters:
        celery (Celery): Celery instance.
        json_key (str): The key used to store the model path during serialization.
        naive_utc (bool): Enable orjson OPT_NAIVE_UTC.
        utc_z (bool): Enable orjson OPT_UTC_Z.
    """
    global json_module_key
    global orjson_opts

    json_module_key = json_key

    if naive_utc:
        orjson_opts |= orjson.OPT_NAIVE_UTC

    if utc_z:
        orjson_opts |= orjson.OPT_UTC_Z

    celery.conf.accept_content = ["json+sqlalchemy"]
    celery.conf.result_accept_content = ["json+sqlalchemy"]
    celery.conf.task_serializer = "json+sqlalchemy"

    serialization.register(
        "json+sqlalchemy",
        message_from_args,
        message_to_args,
        "json",
    )


def message_from_args(args: Union[str, Dict[str, Any], List[Any]]) -> bytes:
    """
    Serialize arguments into their message equivalent.

    Parameters:
        args (dict): Task arguments.
    """
    return orjson.dumps(args, default=arg_to_json, option=orjson_opts)


def message_to_args(
    message: Union[bytes, str]
) -> Union[str, Dict[str, Any], List[Any]]:
    """
    Deserialize a message into its python argument equivalent.

    Parameters:
        message (bytes | str): Message.
    """
    data = orjson.loads(message)

    try:
        args = data[0]
        kwargs = data[1]

        for arg_n, arg_v in enumerate(args):
            args[arg_n] = arg_from_json(arg_v)

        for arg_k, arg_v in kwargs.items():
            kwargs[arg_k] = arg_from_json(arg_v)

    except KeyError:
        # celery to celery message
        pass

    return data


# --------------------------------------------------------------------------------------
# Params helpers
# --------------------------------------------------------------------------------------

NumericParams = namedtuple(
    "NumericParams", "precision scale decimal_return_scale asdecimal"
)

# --------------------------------------------------------------------------------------
# Standard serialization functions
# --------------------------------------------------------------------------------------


def array_from_json(field: Field, value: Optional[List[Any]]) -> Optional[List[Any]]:
    return value


def array_params(column: Column) -> Any:
    return


def array_to_json(field: Field, value: Optional[List[Any]]) -> Optional[List[Any]]:
    return value


def big_integer_from_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def big_integer_params(column: Column) -> Any:
    return


def big_integer_to_json(field: Field, value: Optional[int]) -> Optional[int]:
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


def date_out_params(column: Column) -> Any:
    return


def date_to_json(field: Field, value: Optional[date]) -> Optional[date]:
    return value


def date_time_from_json(field: Field, value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None

    return datetime.fromisoformat(value)


def date_time_params(column: Column) -> Any:
    return


def date_time_to_json(field: Field, value: Optional[datetime]) -> Optional[datetime]:
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


def large_binary_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def large_binary_params(column: Column) -> Any:
    return


def large_binary_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
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


def small_integer_from_json(field: Field, value: Optional[int]) -> Optional[int]:
    return value


def small_integer_params(column: Column) -> Any:
    return


def small_integer_to_json(field: Field, value: Optional[int]) -> Optional[int]:
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


def unicode_text_from_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def unicode_text_params(column: Column) -> Any:
    return


def unicode_text_to_json(field: Field, value: Optional[str]) -> Optional[str]:
    return value


def uuid_from_json(field: Field, value: Optional[str]) -> Optional[UUID]:
    if value is None:
        return None

    return UUID(value)


def uuid_params(column: Column) -> Any:
    return


def uuid_to_json(field: Field, value: Optional[UUID]) -> Optional[UUID]:
    return value


# --------------------------------------------------------------------------------------
# Dialect specific serialization functions
# --------------------------------------------------------------------------------------


def postgresql_array_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_array_params(column: Column) -> Any:
    return


def postgresql_array_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_daterange_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_daterange_params(column: Column) -> Any:
    return


def postgresql_daterange_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_datemultirange_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_datemultirange_params(column: Column) -> Any:
    return


def postgresql_datemultirange_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_enum_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_enum_params(column: Column) -> Any:
    return


def postgresql_enum_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_hstore_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_hstore_params(column: Column) -> Any:
    return


def postgresql_hstore_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4range_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4range_params(column: Column) -> Any:
    return


def postgresql_int4range_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4multirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int4multirange_params(column: Column) -> Any:
    return


def postgresql_int4multirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int8range_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int8range_params(column: Column) -> Any:
    return


def postgresql_int8range_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int8multirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int8multirange_params(column: Column) -> Any:
    return


def postgresql_int8multirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_json_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_json_params(column: Column) -> Any:
    return


def postgresql_json_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonb_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonb_params(column: Column) -> Any:
    return


def postgresql_jsonb_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonpath_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonpath_params(column: Column) -> Any:
    return


def postgresql_jsonpath_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_numrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_numrange_params(column: Column) -> Any:
    return


def postgresql_numrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_nummultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_nummultirange_params(column: Column) -> Any:
    return


def postgresql_nummultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tsrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsrange_params(column: Column) -> Any:
    return


def postgresql_tsrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsmultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tsmultirange_params(column: Column) -> Any:
    return


def postgresql_tsmultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tstzrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tstzrange_params(column: Column) -> Any:
    return


def postgresql_tstzrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tstzmultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tstzmultirange_params(column: Column) -> Any:
    return


def postgresql_tstzmultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value
