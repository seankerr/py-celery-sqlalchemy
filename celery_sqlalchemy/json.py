# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .model import schema_for_model
from .model import schema_for_model_path
from .model import schema_map_key

from .schema import Field

# system imports
from datetime import date
from datetime import datetime
from datetime import time

from decimal import Decimal

from typing import Any
from typing import Dict
from typing import List
from typing import Union

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
                field.name: field.value_in(field, arg.get(field.name))
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
                field.name: field.value_out(field, getattr(arg, field.name))
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
    utc_z: bool = True,
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
# Standard serialization functions
# --------------------------------------------------------------------------------------


def array_in(field: Field, value: Any) -> Any:
    return value


def array_out(field: Field, value: Any) -> Any:
    return value


def array_params(column: Column) -> Any:
    return


def big_integer_in(field: Field, value: Any) -> Any:
    return value


def big_integer_out(field: Field, value: Any) -> Any:
    return value


def big_integer_params(column: Column) -> Any:
    return


def boolean_in(field: Field, value: Any) -> Any:
    return value


def boolean_out(field: Field, value: Any) -> Any:
    return value


def boolean_params(column: Column) -> Any:
    return


def date_in(field: Field, value: Any) -> Any:
    return date.fromisoformat(value)


def date_out(field: Field, value: Any) -> Any:
    return value


def date_out_params(column: Column) -> Any:
    return


def date_time_in(field: Field, value: Any) -> Any:
    if value is None:
        return None

    return datetime.fromisoformat(value)


def date_time_out(field: Field, value: Any) -> Any:
    return value


def date_time_params(column: Column) -> Any:
    return


def double_in(field: Field, value: Any) -> Any:
    return value


def double_out(field: Field, value: Any) -> Any:
    return value


def double_params(column: Column) -> Any:
    return


def enum_in(field: Field, value: Any) -> Any:
    return value


def enum_out(field: Field, value: Any) -> Any:
    return value


def enum_params(column: Column) -> Any:
    return


def float_in(field: Field, value: Any) -> Any:
    return value


def float_out(field: Field, value: Any) -> Any:
    return value


def float_params(column: Column) -> Any:
    return


def integer_in(field: Field, value: Any) -> Any:
    return value


def integer_out(field: Field, value: Any) -> Any:
    return value


def integer_params(column: Column) -> Any:
    return


def interval_in(field: Field, value: Any) -> Any:
    return value


def interval_out(field: Field, value: Any) -> Any:
    return value


def interval_params(column: Column) -> Any:
    return


def large_binary_in(field: Field, value: Any) -> Any:
    return value


def large_binary_out(field: Field, value: Any) -> Any:
    return value


def large_binary_params(column: Column) -> Any:
    return


def json_in(field: Field, value: Any) -> Any:
    return value


def json_out(field: Field, value: Any) -> Any:
    return value


def json_params(column: Column) -> Any:
    return


def numeric_in(field: Field, value: Any) -> Any:
    return Decimal(value)


def numeric_out(field: Field, value: Any) -> Any:
    return str(value)


def numeric_params(column: Column) -> Any:
    return


def small_integer_in(field: Field, value: Any) -> Any:
    return value


def small_integer_out(field: Field, value: Any) -> Any:
    return value


def small_integer_params(column: Column) -> Any:
    return


def string_in(field: Field, value: Any) -> Any:
    return value


def string_out(field: Field, value: Any) -> Any:
    return value


def string_params(column: Column) -> Any:
    return


def text_in(field: Field, value: Any) -> Any:
    return value


def text_out(field: Field, value: Any) -> Any:
    return value


def text_params(column: Column) -> Any:
    return


def time_in(field: Field, value: Any) -> Any:
    return time.fromisoformat(value)


def time_out(field: Field, value: Any) -> Any:
    return value


def time_params(column: Column) -> Any:
    return


def unicode_in(field: Field, value: Any) -> Any:
    return value


def unicode_out(field: Field, value: Any) -> Any:
    return value


def unicode_params(column: Column) -> Any:
    return


def unicode_text_in(field: Field, value: Any) -> Any:
    return value


def unicode_text_out(field: Field, value: Any) -> Any:
    return value


def unicode_text_params(column: Column) -> Any:
    return


def uuid_in(field: Field, value: Any) -> Any:
    return UUID(value)


def uuid_out(field: Field, value: Any) -> Any:
    return value


def uuid_params(column: Column) -> Any:
    return


# --------------------------------------------------------------------------------------
# Dialect specific serialization functions
# --------------------------------------------------------------------------------------


def postgresql_array_in(field: Field, value: Any) -> Any:
    return value


def postgresql_array_out(field: Field, value: Any) -> Any:
    return value


def postgresql_enum_in(field: Field, value: Any) -> Any:
    return value


def postgresql_enum_out(field: Field, value: Any) -> Any:
    return value


def postgresql_hstore_in(field: Field, value: Any) -> Any:
    return value


def postgresql_hstore_out(field: Field, value: Any) -> Any:
    return value


def postgresql_json_in(field: Field, value: Any) -> Any:
    return value


def postgresql_json_out(field: Field, value: Any) -> Any:
    return value


def postgresql_jsonb_in(field: Field, value: Any) -> Any:
    return value


def postgresql_jsonb_out(field: Field, value: Any) -> Any:
    return value
