# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import TypeMap
from celery_sqlalchemy.model import map_model
from celery_sqlalchemy.model import type_maps

from celery_sqlalchemy.schema import Field

# system imports
from typing import Any
from typing import List

from unittest.mock import Mock

# dependency imports
from pytest import mark

from sqlalchemy.dialects.postgresql.array import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql.named_types import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql.hstore import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql.json import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql.json import JSONB as POSTGRESQL_JSONB

from sqlalchemy.sql import sqltypes


@mark.parametrize("type", type_maps.keys())
def testmap_model(type: type) -> None:
    column = Mock(type=Mock(__class__=type))
    model = Mock()
    mapper = Mock(columns=[column])
    format_module = Mock()

    value_in = Mock()
    value_out = Mock()

    setattr(format_module, type_maps[type].value_in, value_in)
    setattr(format_module, type_maps[type].value_out, value_out)

    schema = map_model(model, mapper, format_module)

    assert schema.fields == [
        Field(
            name=column.name,
            type=type,
            value_in=value_in,
            value_out=value_out,
        )
    ]

    assert schema.model == model


@mark.parametrize(
    "type",
    [
        [sqltypes.ARRAY, "array_in", "array_out"],
        [sqltypes.BigInteger, "big_integer_in", "big_integer_out"],
        [sqltypes.Boolean, "boolean_in", "boolean_out"],
        [sqltypes.Date, "date_in", "date_out"],
        [sqltypes.DateTime, "date_time_in", "date_time_out"],
        [sqltypes.Double, "double_in", "double_out"],
        [sqltypes.Enum, "enum_in", "enum_out"],
        [sqltypes.Float, "float_in", "float_out"],
        [sqltypes.Integer, "integer_in", "integer_out"],
        [sqltypes.Interval, "interval_in", "interval_out"],
        [sqltypes.LargeBinary, "large_binary_in", "large_binary_out"],
        [sqltypes.JSON, "json_in", "json_out"],
        [sqltypes.Numeric, "numeric_in", "numeric_out"],
        [sqltypes.SmallInteger, "small_integer_in", "small_integer_out"],
        [sqltypes.String, "string_in", "string_out"],
        [sqltypes.Text, "text_in", "text_out"],
        [sqltypes.Time, "time_in", "time_out"],
        [sqltypes.Unicode, "unicode_in", "unicode_out"],
        [sqltypes.UnicodeText, "unicode_text_in", "unicode_text_out"],
        [sqltypes.UUID, "uuid_in", "uuid_out"],
        [POSTGRESQL_ARRAY, "postgresql_array_in", "postgresql_array_out"],
        [POSTGRESQL_ENUM, "postgresql_enum_in", "postgresql_enum_out"],
        [POSTGRESQL_HSTORE, "postgresql_hstore_in", "postgresql_hstore_out"],
        [POSTGRESQL_JSON, "postgresql_json_in", "postgresql_json_out"],
        [POSTGRESQL_JSONB, "postgresql_jsonb_in", "postgresql_jsonb_out"],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert type_maps[type[0]] == TypeMap(value_in=type[1], value_out=type[2])
