# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..model import schema_for_model
from ..model import schema_for_model_path
from ..model import schema_map_key

from .. import errors

# system imports
from collections.abc import Iterable

from collections import namedtuple

from typing import Any
from typing import Dict
from typing import List
from typing import Union

import sys

# dependency imports
from celery import Celery

from kombu import serialization

from sqlalchemy.exc import NoInspectionAvailable

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

    elif isinstance(arg, Iterable):
        return [arg_from_json(item) for item in arg]

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
            pass

    elif isinstance(arg, set):
        return list(arg)

    raise errors.SerializationError(f"Cannot serialize type '{arg.__class__.__name__}'")


def initialize(
    celery: Celery,
    json_key: str = "$model_path$",
    content_type: str = "json+sqlalchemy",
    apply_serializer: bool = True,
    naive_utc: bool = True,
    utc_z: bool = False,
) -> None:
    """
    Initialize the JSON module.

    Parameters:
        celery (Celery): Celery instance.
        json_key (str): The key used to store the model path during serialization.
        content_type (str): The content type to use for this serializer.
        apply_serializer (bool): Apply the task serializer settings globally.
        naive_utc (bool): Enable orjson OPT_NAIVE_UTC.
        utc_z (bool): Enable orjson OPT_UTC_Z.
    """
    global json_module_key
    global orjson_opts

    json_module_key = json_key
    orjson_opts = 0

    if naive_utc:
        orjson_opts |= orjson.OPT_NAIVE_UTC

    if utc_z:
        orjson_opts |= orjson.OPT_UTC_Z

    serialization.register(
        content_type,
        message_from_args,
        message_to_args,
        "json",
    )

    if apply_serializer:
        celery.conf.accept_content = [content_type]
        celery.conf.result_accept_content = [content_type]
        celery.conf.task_serializer = content_type


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

from .sqlalchemy import array_from_json  # noqa
from .sqlalchemy import array_params  # noqa
from .sqlalchemy import array_to_json  # noqa
from .sqlalchemy import biginteger_from_json  # noqa
from .sqlalchemy import biginteger_params  # noqa
from .sqlalchemy import biginteger_to_json  # noqa
from .sqlalchemy import boolean_from_json  # noqa
from .sqlalchemy import boolean_params  # noqa
from .sqlalchemy import boolean_to_json  # noqa
from .sqlalchemy import date_from_json  # noqa
from .sqlalchemy import date_params  # noqa
from .sqlalchemy import date_to_json  # noqa
from .sqlalchemy import datetime_from_json  # noqa
from .sqlalchemy import datetime_params  # noqa
from .sqlalchemy import datetime_to_json  # noqa
from .sqlalchemy import double_from_json  # noqa
from .sqlalchemy import double_params  # noqa
from .sqlalchemy import double_to_json  # noqa
from .sqlalchemy import enum_from_json  # noqa
from .sqlalchemy import enum_params  # noqa
from .sqlalchemy import enum_to_json  # noqa
from .sqlalchemy import float_from_json  # noqa
from .sqlalchemy import float_params  # noqa
from .sqlalchemy import float_to_json  # noqa
from .sqlalchemy import integer_from_json  # noqa
from .sqlalchemy import integer_params  # noqa
from .sqlalchemy import integer_to_json  # noqa
from .sqlalchemy import interval_from_json  # noqa
from .sqlalchemy import interval_params  # noqa
from .sqlalchemy import interval_to_json  # noqa
from .sqlalchemy import largebinary_from_json  # noqa
from .sqlalchemy import largebinary_params  # noqa
from .sqlalchemy import largebinary_to_json  # noqa
from .sqlalchemy import json_from_json  # noqa
from .sqlalchemy import json_params  # noqa
from .sqlalchemy import json_to_json  # noqa
from .sqlalchemy import numeric_from_json  # noqa
from .sqlalchemy import numeric_params  # noqa
from .sqlalchemy import numeric_to_json  # noqa
from .sqlalchemy import smallinteger_from_json  # noqa
from .sqlalchemy import smallinteger_params  # noqa
from .sqlalchemy import smallinteger_to_json  # noqa
from .sqlalchemy import string_from_json  # noqa
from .sqlalchemy import string_params  # noqa
from .sqlalchemy import string_to_json  # noqa
from .sqlalchemy import text_from_json  # noqa
from .sqlalchemy import text_params  # noqa
from .sqlalchemy import text_to_json  # noqa
from .sqlalchemy import time_from_json  # noqa
from .sqlalchemy import time_params  # noqa
from .sqlalchemy import time_to_json  # noqa
from .sqlalchemy import unicode_from_json  # noqa
from .sqlalchemy import unicode_params  # noqa
from .sqlalchemy import unicode_to_json  # noqa
from .sqlalchemy import unicodetext_from_json  # noqa
from .sqlalchemy import unicodetext_params  # noqa
from .sqlalchemy import unicodetext_to_json  # noqa
from .sqlalchemy import uuid_from_json  # noqa
from .sqlalchemy import uuid_params  # noqa
from .sqlalchemy import uuid_to_json  # noqa

# --------------------------------------------------------------------------------------
# PostgreSQL serialization functions
# --------------------------------------------------------------------------------------

from .postgresql import postgresql_array_from_json  # noqa
from .postgresql import postgresql_array_params  # noqa
from .postgresql import postgresql_array_to_json  # noqa
from .postgresql import postgresql_bit_from_json  # noqa
from .postgresql import postgresql_bit_params  # noqa
from .postgresql import postgresql_bit_to_json  # noqa
from .postgresql import postgresql_bytea_from_json  # noqa
from .postgresql import postgresql_bytea_params  # noqa
from .postgresql import postgresql_bytea_to_json  # noqa
from .postgresql import postgresql_cidr_from_json  # noqa
from .postgresql import postgresql_cidr_params  # noqa
from .postgresql import postgresql_cidr_to_json  # noqa
from .postgresql import postgresql_citext_from_json  # noqa
from .postgresql import postgresql_citext_params  # noqa
from .postgresql import postgresql_citext_to_json  # noqa
from .postgresql import postgresql_daterange_from_json  # noqa
from .postgresql import postgresql_daterange_params  # noqa
from .postgresql import postgresql_daterange_to_json  # noqa
from .postgresql import postgresql_datemultirange_from_json  # noqa
from .postgresql import postgresql_datemultirange_params  # noqa
from .postgresql import postgresql_datemultirange_to_json  # noqa
from .postgresql import postgresql_domain_from_json  # noqa
from .postgresql import postgresql_domain_params  # noqa
from .postgresql import postgresql_domain_to_json  # noqa
from .postgresql import postgresql_double_precision_from_json  # noqa
from .postgresql import postgresql_double_precision_params  # noqa
from .postgresql import postgresql_double_precision_to_json  # noqa
from .postgresql import postgresql_enum_from_json  # noqa
from .postgresql import postgresql_enum_params  # noqa
from .postgresql import postgresql_enum_to_json  # noqa
from .postgresql import postgresql_hstore_from_json  # noqa
from .postgresql import postgresql_hstore_params  # noqa
from .postgresql import postgresql_hstore_to_json  # noqa
from .postgresql import postgresql_int4range_from_json  # noqa
from .postgresql import postgresql_int4range_params  # noqa
from .postgresql import postgresql_int4range_to_json  # noqa
from .postgresql import postgresql_int4multirange_from_json  # noqa
from .postgresql import postgresql_int4multirange_params  # noqa
from .postgresql import postgresql_int4multirange_to_json  # noqa
from .postgresql import postgresql_int8range_from_json  # noqa
from .postgresql import postgresql_int8range_params  # noqa
from .postgresql import postgresql_int8range_to_json  # noqa
from .postgresql import postgresql_int8multirange_from_json  # noqa
from .postgresql import postgresql_int8multirange_params  # noqa
from .postgresql import postgresql_int8multirange_to_json  # noqa
from .postgresql import postgresql_inet_from_json  # noqa
from .postgresql import postgresql_inet_params  # noqa
from .postgresql import postgresql_inet_to_json  # noqa
from .postgresql import postgresql_interval_from_json  # noqa
from .postgresql import postgresql_interval_params  # noqa
from .postgresql import postgresql_interval_to_json  # noqa
from .postgresql import postgresql_json_from_json  # noqa
from .postgresql import postgresql_json_params  # noqa
from .postgresql import postgresql_json_to_json  # noqa
from .postgresql import postgresql_jsonb_from_json  # noqa
from .postgresql import postgresql_jsonb_params  # noqa
from .postgresql import postgresql_jsonb_to_json  # noqa
from .postgresql import postgresql_jsonpath_from_json  # noqa
from .postgresql import postgresql_jsonpath_params  # noqa
from .postgresql import postgresql_jsonpath_to_json  # noqa
from .postgresql import postgresql_macaddr_from_json  # noqa
from .postgresql import postgresql_macaddr_params  # noqa
from .postgresql import postgresql_macaddr_to_json  # noqa
from .postgresql import postgresql_macaddr8_from_json  # noqa
from .postgresql import postgresql_macaddr8_params  # noqa
from .postgresql import postgresql_macaddr8_to_json  # noqa
from .postgresql import postgresql_money_from_json  # noqa
from .postgresql import postgresql_money_params  # noqa
from .postgresql import postgresql_money_to_json  # noqa
from .postgresql import postgresql_numrange_from_json  # noqa
from .postgresql import postgresql_numrange_params  # noqa
from .postgresql import postgresql_numrange_to_json  # noqa
from .postgresql import postgresql_nummultirange_from_json  # noqa
from .postgresql import postgresql_nummultirange_params  # noqa
from .postgresql import postgresql_nummultirange_to_json  # noqa
from .postgresql import postgresql_oid_from_json  # noqa
from .postgresql import postgresql_oid_params  # noqa
from .postgresql import postgresql_oid_to_json  # noqa
from .postgresql import postgresql_real_from_json  # noqa
from .postgresql import postgresql_real_params  # noqa
from .postgresql import postgresql_real_to_json  # noqa
from .postgresql import postgresql_regclass_from_json  # noqa
from .postgresql import postgresql_regclass_params  # noqa
from .postgresql import postgresql_regclass_to_json  # noqa
from .postgresql import postgresql_regconfig_from_json  # noqa
from .postgresql import postgresql_regconfig_params  # noqa
from .postgresql import postgresql_regconfig_to_json  # noqa
from .postgresql import postgresql_time_from_json  # noqa
from .postgresql import postgresql_time_params  # noqa
from .postgresql import postgresql_time_to_json  # noqa
from .postgresql import postgresql_timestamp_from_json  # noqa
from .postgresql import postgresql_timestamp_params  # noqa
from .postgresql import postgresql_timestamp_to_json  # noqa
from .postgresql import postgresql_tsquery_from_json  # noqa
from .postgresql import postgresql_tsquery_params  # noqa
from .postgresql import postgresql_tsquery_to_json  # noqa
from .postgresql import postgresql_tsrange_from_json  # noqa
from .postgresql import postgresql_tsrange_params  # noqa
from .postgresql import postgresql_tsrange_to_json  # noqa
from .postgresql import postgresql_tsmultirange_from_json  # noqa
from .postgresql import postgresql_tsmultirange_params  # noqa
from .postgresql import postgresql_tsmultirange_to_json  # noqa
from .postgresql import postgresql_tstzrange_from_json  # noqa
from .postgresql import postgresql_tstzrange_params  # noqa
from .postgresql import postgresql_tstzrange_to_json  # noqa
from .postgresql import postgresql_tstzmultirange_from_json  # noqa
from .postgresql import postgresql_tstzmultirange_params  # noqa
from .postgresql import postgresql_tstzmultirange_to_json  # noqa
from .postgresql import postgresql_tsvector_from_json  # noqa
from .postgresql import postgresql_tsvector_params  # noqa
from .postgresql import postgresql_tsvector_to_json  # noqa
