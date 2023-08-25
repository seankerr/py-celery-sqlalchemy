# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import TypeMap

# dependency imports
from sqlalchemy.sql import sqltypes

sqlalchemy_type_maps = {
    sqltypes.ARRAY: TypeMap(
        from_json="array_from_json", params="array_params", to_json="array_to_json"
    ),
    sqltypes.BigInteger: TypeMap(
        from_json="biginteger_from_json",
        params="biginteger_params",
        to_json="biginteger_to_json",
    ),
    sqltypes.Boolean: TypeMap(
        from_json="boolean_from_json",
        params="boolean_params",
        to_json="boolean_to_json",
    ),
    sqltypes.Date: TypeMap(
        from_json="date_from_json", params="date_params", to_json="date_to_json"
    ),
    sqltypes.DateTime: TypeMap(
        from_json="datetime_from_json",
        params="datetime_params",
        to_json="datetime_to_json",
    ),
    sqltypes.Double: TypeMap(
        from_json="double_from_json", params="double_params", to_json="double_to_json"
    ),
    sqltypes.Enum: TypeMap(
        from_json="enum_from_json", params="enum_params", to_json="enum_to_json"
    ),
    sqltypes.Float: TypeMap(
        from_json="float_from_json", params="float_params", to_json="float_to_json"
    ),
    sqltypes.Integer: TypeMap(
        from_json="integer_from_json",
        params="integer_params",
        to_json="integer_to_json",
    ),
    sqltypes.Interval: TypeMap(
        from_json="interval_from_json",
        params="interval_params",
        to_json="interval_to_json",
    ),
    sqltypes.LargeBinary: TypeMap(
        from_json="largebinary_from_json",
        params="largebinary_params",
        to_json="largebinary_to_json",
    ),
    sqltypes.JSON: TypeMap(
        from_json="json_from_json", params="json_params", to_json="json_to_json"
    ),
    sqltypes.Numeric: TypeMap(
        from_json="numeric_from_json",
        params="numeric_params",
        to_json="numeric_to_json",
    ),
    sqltypes.SmallInteger: TypeMap(
        from_json="smallinteger_from_json",
        params="smallinteger_params",
        to_json="smallinteger_to_json",
    ),
    sqltypes.String: TypeMap(
        from_json="string_from_json", params="string_params", to_json="string_to_json"
    ),
    sqltypes.Text: TypeMap(
        from_json="text_from_json", params="text_params", to_json="text_to_json"
    ),
    sqltypes.Time: TypeMap(
        from_json="time_from_json", params="time_params", to_json="time_to_json"
    ),
    sqltypes.Unicode: TypeMap(
        from_json="unicode_from_json",
        params="unicode_params",
        to_json="unicode_to_json",
    ),
    sqltypes.UnicodeText: TypeMap(
        from_json="unicodetext_from_json",
        params="unicodetext_params",
        to_json="unicodetext_to_json",
    ),
    sqltypes.UUID: TypeMap(
        from_json="uuid_from_json", params="uuid_params", to_json="uuid_to_json"
    ),
}
