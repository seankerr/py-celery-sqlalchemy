# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model.sqlalchemy import sqlalchemy_type_maps

from celery_sqlalchemy.schema import TypeMap

# system imports
from typing import Any
from typing import List

# dependency imports
from pytest import mark

from sqlalchemy.sql import sqltypes


@mark.parametrize(
    "type",
    [
        [sqltypes.ARRAY, "array_from_json", "array_params", "array_to_json"],
        [
            sqltypes.BigInteger,
            "biginteger_from_json",
            "biginteger_params",
            "biginteger_to_json",
        ],
        [sqltypes.Boolean, "boolean_from_json", "boolean_params", "boolean_to_json"],
        [sqltypes.Date, "date_from_json", "date_params", "date_to_json"],
        [
            sqltypes.DateTime,
            "datetime_from_json",
            "datetime_params",
            "datetime_to_json",
        ],
        [sqltypes.Double, "double_from_json", "double_params", "double_to_json"],
        [sqltypes.Enum, "enum_from_json", "enum_params", "enum_to_json"],
        [sqltypes.Float, "float_from_json", "float_params", "float_to_json"],
        [sqltypes.Integer, "integer_from_json", "integer_params", "integer_to_json"],
        [
            sqltypes.Interval,
            "interval_from_json",
            "interval_params",
            "interval_to_json",
        ],
        [
            sqltypes.LargeBinary,
            "largebinary_from_json",
            "largebinary_params",
            "largebinary_to_json",
        ],
        [sqltypes.JSON, "json_from_json", "json_params", "json_to_json"],
        [sqltypes.Numeric, "numeric_from_json", "numeric_params", "numeric_to_json"],
        [
            sqltypes.SmallInteger,
            "smallinteger_from_json",
            "smallinteger_params",
            "smallinteger_to_json",
        ],
        [sqltypes.String, "string_from_json", "string_params", "string_to_json"],
        [sqltypes.Text, "text_from_json", "text_params", "text_to_json"],
        [sqltypes.Time, "time_from_json", "time_params", "time_to_json"],
        [sqltypes.Unicode, "unicode_from_json", "unicode_params", "unicode_to_json"],
        [
            sqltypes.UnicodeText,
            "unicodetext_from_json",
            "unicodetext_params",
            "unicodetext_to_json",
        ],
        [sqltypes.UUID, "uuid_from_json", "uuid_params", "uuid_to_json"],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert sqlalchemy_type_maps[type[0]] == TypeMap(
        from_json=type[1], params=type[2], to_json=type[3]
    )
