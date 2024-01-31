# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..model import schema_for_model
from ..model import schema_for_model_path
from ..model import schema_map_key

from ..types import Args
from ..types import Message
from ..types import Serializer

from .. import errors

# system imports
from collections import namedtuple

from typing import Any
from typing import Callable
from typing import Optional

import sys

# dependency imports
from sqlalchemy.exc import NoInspectionAvailable

from sqlalchemy import inspect

import orjson


class JsonSerializer(Serializer):
    def __init__(
        self,
        json_key: str = "$model_path$",
        naive_utc: bool = True,
        passthrough_dataclass: bool = False,
        utc_z: bool = False,
        on_deserialize_arg: Optional[Callable] = None,
        on_serialize_arg: Optional[Callable] = None,
    ) -> None:
        """
        Initialize the JSON module.

        Parameters:
            json_key (str): The key used to store the model path during serialization.
            naive_utc (bool): Enable orjson OPT_NAIVE_UTC.
            passthrough_dataclass (bool): Enable orjson OPT_PASSTHROUGH_DATACLASS.
            utc_z (bool): Enable orjson OPT_UTC_Z.
            on_deserialize_arg (Callback): Deserialization callback.
            on_serialize_arg (Callback): Serialization callback.
        """
        self.deserialize_arg = on_deserialize_arg
        self.json_key = json_key
        self.orjson_opts = 0
        self.serialize_arg = on_serialize_arg

        if naive_utc:
            self.orjson_opts |= orjson.OPT_NAIVE_UTC

        if passthrough_dataclass:
            self.orjson_opts |= orjson.OPT_PASSTHROUGH_DATACLASS

        if utc_z:
            self.orjson_opts |= orjson.OPT_UTC_Z

    def arg_from_json(self, arg: Any) -> Any:
        """
        Deserialize a JSON argument into its python equivalent.

        Parameters:
            arg (object): Any object type.
        """
        if isinstance(arg, dict) and self.json_key in arg:
            schema = schema_for_model_path(arg[self.json_key], sys.modules[__name__])
            model = (
                schema.model
                if isinstance(schema.model, type)
                else schema.model.__class__
            )

            return model(
                **{
                    field.name: field.from_json(field, arg.get(field.name))
                    for field in schema.fields
                }
            )

        elif isinstance(arg, list):
            return [self.arg_from_json(item) for item in arg]

        elif self.deserialize_arg:
            return self.deserialize_arg(arg)

        else:
            return arg

    def arg_to_json(self, arg: Any) -> Any:
        """
        Serialize a python argument into its JSON equivalent.

        Parameters:
            arg (object): Any object type.

        Raises:
            errors.SerializationError: If the argument cannot be serialized.
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

                json[self.json_key] = schema_map_key(arg)

                return json

            except NoInspectionAvailable:
                pass

        elif isinstance(arg, set):
            return list(arg)

        if self.serialize_arg:
            return self.serialize_arg(arg)

        raise errors.SerializationError(
            f"Cannot serialize type '{arg.__class__.__name__}'"
        )

    def message_from_args(self, args: Args) -> Message:
        """
        Serialize python arguments into their message equivalent.

        Parameters:
            args (dict): Arguments.
        """
        return orjson.dumps(
            {
                "$arg$": args.arg,
                "$args$": args.args,
                "$kwargs$": args.kwargs,
            },
            default=self.arg_to_json,
            option=self.orjson_opts,
        )

    def message_to_args(self, message: Message) -> Args:
        """
        Deserialize a message into its python equivalent.

        Parameters:
            message (Message): Message.
        """
        json = orjson.loads(message)
        args = Args(
            arg=self.arg_from_json(json["$arg$"]),
            args=json["$args$"],
            kwargs=json["$kwargs$"],
        )

        if args.args:
            for arg_n, arg_v in enumerate(args.args):
                args.args[arg_n] = self.arg_from_json(arg_v)

        if args.kwargs:
            for arg_k, arg_v in args.kwargs.items():
                args.kwargs[arg_k] = self.arg_from_json(arg_v)

        return args


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
