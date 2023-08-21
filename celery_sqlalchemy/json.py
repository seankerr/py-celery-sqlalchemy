# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .model import schema_for_model
from .model import schema_for_model_path
from .model import schema_map_key

# system imports
from typing import Any
from typing import Dict
from typing import List
from typing import Union

# dependency imports
from celery import Celery

from kombu import serialization

from sqlalchemy.exc import NoInspectionAvailable

from sqlalchemy import inspect

import orjson

json_module_key = ""


def arg_from_json(arg: Any) -> Any:
    """
    Deserialize a single task argument into its python equivalent.

    Parameters:
        arg (object): Any object type.
    """
    if isinstance(arg, dict) and json_module_key in arg:
        try:
            schema = schema_for_model_path(arg[json_module_key])

            return schema.model(
                **{
                    field.name: field.value_in(arg.get(field))
                    for field in schema.fields
                }
            )

        except KeyError:
            return arg

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
            mapper = inspect(arg)
            schema = schema_for_model(arg, mapper)

            json = {
                field.name: field.value_out(getattr(arg, field.name))
                for field in schema.fields
            }

            json[json_module_key] = schema_map_key(arg)

            return json

        except (KeyError, NoInspectionAvailable):
            return arg

    else:
        return arg


def initialize(celery: Celery, json_key: str = "$model_path$") -> None:
    """
    Initialize the JSON module.

    Parameters:
        celery (Celery): Celery instance.
        json_key (str): The key used to store the model path during serialization.
    """
    global json_module_key

    json_module_key = json_key

    celery.conf.accept_content = ["json+sqlalchemy"] + celery.conf.accept_content

    celery.conf.result_accept_content = [
        "json+sqlalchemy"
    ] + celery.conf.result_accept_content

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
    return orjson.dumps(
        args, default=arg_to_json, option=orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z
    )


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


def array_in(value: Any) -> Any:
    return value


def array_out(value: Any) -> Any:
    return value


def big_integer_in(value: Any) -> Any:
    return value


def big_integer_out(value: Any) -> Any:
    return value


def boolean_in(value: Any) -> Any:
    return value


def boolean_out(value: Any) -> Any:
    return value


def date_in(value: Any) -> Any:
    return value


def date_out(value: Any) -> Any:
    return value


def date_time_in(value: Any) -> Any:
    return value


def date_time_out(value: Any) -> Any:
    return value


def double_in(value: Any) -> Any:
    return value


def double_out(value: Any) -> Any:
    return value


def enum_in(value: Any) -> Any:
    return value


def enum_out(value: Any) -> Any:
    return value


def float_in(value: Any) -> Any:
    return value


def float_out(value: Any) -> Any:
    return value


def integer_in(value: Any) -> Any:
    return value


def integer_out(value: Any) -> Any:
    return value


def interval_in(value: Any) -> Any:
    return value


def interval_out(value: Any) -> Any:
    return value


def large_binary_in(value: Any) -> Any:
    return value


def large_binary_out(value: Any) -> Any:
    return value


def json_in(value: Any) -> Any:
    return value


def json_out(value: Any) -> Any:
    return value


def numeric_in(value: Any) -> Any:
    return value


def numeric_out(value: Any) -> Any:
    return value


def small_integer_in(value: Any) -> Any:
    return value


def small_integer_out(value: Any) -> Any:
    return value


def string_in(value: Any) -> Any:
    return value


def string_out(value: Any) -> Any:
    return value


def text_in(value: Any) -> Any:
    return value


def text_out(value: Any) -> Any:
    return value


def time_in(value: Any) -> Any:
    return value


def time_out(value: Any) -> Any:
    return value


def unicode_in(value: Any) -> Any:
    return value


def unicode_out(value: Any) -> Any:
    return value


def unicode_text_in(value: Any) -> Any:
    return value


def unicode_text_out(value: Any) -> Any:
    return value


def uuid_in(value: Any) -> Any:
    return value


def uuid_out(value: Any) -> Any:
    return value


# --------------------------------------------------------------------------------------
# Dialect specific serialization functions
# --------------------------------------------------------------------------------------


def postgresql_array_in(value: Any) -> Any:
    return value


def postgresql_array_out(value: Any) -> Any:
    return value


def postgresql_enum_in(value: Any) -> Any:
    return value


def postgresql_enum_out(value: Any) -> Any:
    return value


def postgresql_hstore_in(value: Any) -> Any:
    return value


def postgresql_hstore_out(value: Any) -> Any:
    return value


def postgresql_json_in(value: Any) -> Any:
    return value


def postgresql_json_out(value: Any) -> Any:
    return value


def postgresql_jsonb_in(value: Any) -> Any:
    return value


def postgresql_jsonb_out(value: Any) -> Any:
    return value
