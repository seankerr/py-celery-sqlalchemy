# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import TypeMap
from celery_sqlalchemy.model import add_schema
from celery_sqlalchemy.model import load_model
from celery_sqlalchemy.model import map_model
from celery_sqlalchemy.model import schema_for_model
from celery_sqlalchemy.model import schema_for_model_path
from celery_sqlalchemy.model import schema_map_key
from celery_sqlalchemy.model import type_maps

from celery_sqlalchemy.schema import Field

# system imports
from typing import Any
from typing import List

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

# dependency imports
from pytest import mark

from sqlalchemy.dialects.postgresql import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql import INT4RANGE as POSTGRESQL_INT4RANGE
from sqlalchemy.dialects.postgresql import INT4MULTIRANGE as POSTGRESQL_INT4MULTIRANGE
from sqlalchemy.dialects.postgresql import INT8RANGE as POSTGRESQL_INT8RANGE
from sqlalchemy.dialects.postgresql import INT8MULTIRANGE as POSTGRESQL_INT8MULTIRANGE
from sqlalchemy.dialects.postgresql import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql import JSONB as POSTGRESQL_JSONB
from sqlalchemy.dialects.postgresql import JSONPATH as POSTGRESQL_JSONPATH
from sqlalchemy.dialects.postgresql import NUMRANGE as POSTGRESQL_NUMRANGE
from sqlalchemy.dialects.postgresql import NUMMULTIRANGE as POSTGRESQL_NUMMULTIRANGE
from sqlalchemy.dialects.postgresql import TSRANGE as POSTGRESQL_TSRANGE
from sqlalchemy.dialects.postgresql import TSMULTIRANGE as POSTGRESQL_TSMULTIRANGE
from sqlalchemy.dialects.postgresql import TSTZRANGE as POSTGRESQL_TSTZRANGE
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE as POSTGRESQL_TSTZMULTIRANGE

from sqlalchemy.sql import sqltypes

PATH = "celery_sqlalchemy.model"


@patch(f"{PATH}.schema_maps")
@patch(f"{PATH}.schema_map_key")
@patch(f"{PATH}.map_model")
def test_add_schema(
    map_model: Mock, schema_map_key: Mock, schema_maps: MagicMock
) -> None:
    model = Mock()
    mapper = Mock()
    interface = Mock()

    assert add_schema(model, mapper, interface) == map_model.return_value

    map_model.assert_called_with(model, mapper, interface)
    schema_map_key.assert_called_with(model)

    schema_maps.__setitem__.assert_called_with(schema_map_key(), map_model())


@patch(f"{PATH}.import_module")
def test_load_model(import_module: Mock) -> None:
    module = Mock()
    import_module.return_value = module

    model_path = "path.Model"

    assert load_model(model_path) == module.Model


@mark.parametrize("type", type_maps.keys())
def test_map_model(type: type) -> None:
    column = Mock(type=Mock(__class__=type))
    model = Mock()
    mapper = Mock(columns=[column])
    format_module = Mock()

    from_json = Mock()
    params = Mock()
    to_json = Mock()

    setattr(format_module, type_maps[type].from_json, from_json)
    setattr(format_module, type_maps[type].params, params)
    setattr(format_module, type_maps[type].to_json, to_json)

    schema = map_model(model, mapper, format_module)

    params.assert_called_with(column)

    assert schema.fields == [
        Field(
            from_json=from_json,
            name=column.name,
            params=params(),
            to_json=to_json,
            type=type,
        )
    ]

    assert schema.model == model


@patch(f"{PATH}.add_schema")
@patch(f"{PATH}.schema_maps")
@patch(f"{PATH}.schema_map_key")
def test_schema_for_model(
    schema_map_key: Mock, schema_maps: Mock, add_schema: Mock
) -> None:
    schema = Mock()
    schema_maps.get.return_value = schema

    model = Mock()
    mapper = Mock()
    interface = Mock()

    assert schema_for_model(model, mapper, interface) == schema

    add_schema.assert_not_called()
    schema_map_key.assert_called_with(model)
    schema_maps.get.assert_called_with(schema_map_key())


@patch(f"{PATH}.add_schema")
@patch(f"{PATH}.schema_maps")
@patch(f"{PATH}.schema_map_key")
def test_schema_for_model__adds_schema(
    schema_map_key: Mock, schema_maps: Mock, add_schema: Mock
) -> None:
    schema = Mock()
    add_schema.return_value = schema
    schema_maps.get.return_value = None

    model = Mock()
    mapper = Mock()
    interface = Mock()

    assert schema_for_model(model, mapper, interface) == schema

    add_schema.assert_called_with(model, mapper, interface)


@patch(f"{PATH}.schema_maps")
def test_schema_for_model_path(schema_maps: Mock) -> None:
    schema = Mock()
    schema_maps.get.return_value = schema
    model_path = Mock()
    interface = Mock()

    assert schema_for_model_path(model_path, interface) == schema

    schema_maps.get.assert_called_with(model_path)


@patch(f"{PATH}.add_schema")
@patch(f"{PATH}.inspect")
@patch(f"{PATH}.load_model")
@patch(f"{PATH}.schema_maps")
def test_schema_for_model_path__adds_schema(
    schema_maps: Mock, load_model: Mock, inspect: Mock, add_schema: Mock
) -> None:
    model = Mock()
    load_model.return_value = model
    mapper = Mock()
    inspect.return_value = mapper
    schema = Mock()
    add_schema.return_value = schema
    schema_maps.get.return_value = None
    model_path = Mock()
    interface = Mock()

    assert schema_for_model_path(model_path, interface) == schema

    load_model.assert_called_with(model_path)
    inspect.assert_called_with(model)
    add_schema.assert_called_with(model, mapper, interface)


def test_schema_map_key() -> None:
    model = Mock()

    assert schema_map_key(model) == f"{model.__module__}.{model.__class__.__name__}"


@mark.parametrize(
    "type",
    [
        [sqltypes.ARRAY, "array_from_json", "array_params", "array_to_json"],
        [
            sqltypes.BigInteger,
            "big_integer_from_json",
            "big_integer_params",
            "big_integer_to_json",
        ],
        [sqltypes.Boolean, "boolean_from_json", "boolean_params", "boolean_to_json"],
        [sqltypes.Date, "date_from_json", "date_params", "date_to_json"],
        [
            sqltypes.DateTime,
            "date_time_from_json",
            "date_time_params",
            "date_time_to_json",
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
            "large_binary_from_json",
            "large_binary_params",
            "large_binary_to_json",
        ],
        [sqltypes.JSON, "json_from_json", "json_params", "json_to_json"],
        [sqltypes.Numeric, "numeric_from_json", "numeric_params", "numeric_to_json"],
        [
            sqltypes.SmallInteger,
            "small_integer_from_json",
            "small_integer_params",
            "small_integer_to_json",
        ],
        [sqltypes.String, "string_from_json", "string_params", "string_to_json"],
        [sqltypes.Text, "text_from_json", "text_params", "text_to_json"],
        [sqltypes.Time, "time_from_json", "time_params", "time_to_json"],
        [sqltypes.Unicode, "unicode_from_json", "unicode_params", "unicode_to_json"],
        [
            sqltypes.UnicodeText,
            "unicode_text_from_json",
            "unicode_text_params",
            "unicode_text_to_json",
        ],
        [sqltypes.UUID, "uuid_from_json", "uuid_params", "uuid_to_json"],
        [
            POSTGRESQL_ARRAY,
            "postgresql_array_from_json",
            "postgresql_array_params",
            "postgresql_array_to_json",
        ],
        [
            POSTGRESQL_ENUM,
            "postgresql_enum_from_json",
            "postgresql_enum_params",
            "postgresql_enum_to_json",
        ],
        [
            POSTGRESQL_HSTORE,
            "postgresql_hstore_from_json",
            "postgresql_hstore_params",
            "postgresql_hstore_to_json",
        ],
        [
            POSTGRESQL_INT4RANGE,
            "postgresql_int4range_from_json",
            "postgresql_int4range_params",
            "postgresql_int4range_to_json",
        ],
        [
            POSTGRESQL_INT4MULTIRANGE,
            "postgresql_int4multirange_from_json",
            "postgresql_int4multirange_params",
            "postgresql_int4multirange_to_json",
        ],
        [
            POSTGRESQL_INT8RANGE,
            "postgresql_int8range_from_json",
            "postgresql_int8range_params",
            "postgresql_int8range_to_json",
        ],
        [
            POSTGRESQL_INT8MULTIRANGE,
            "postgresql_int8multirange_from_json",
            "postgresql_int8multirange_params",
            "postgresql_int8multirange_to_json",
        ],
        [
            POSTGRESQL_JSON,
            "postgresql_json_from_json",
            "postgresql_json_params",
            "postgresql_json_to_json",
        ],
        [
            POSTGRESQL_JSONB,
            "postgresql_jsonb_from_json",
            "postgresql_jsonb_params",
            "postgresql_jsonb_to_json",
        ],
        [
            POSTGRESQL_JSONPATH,
            "postgresql_jsonpath_from_json",
            "postgresql_jsonpath_params",
            "postgresql_jsonpath_to_json",
        ],
        [
            POSTGRESQL_NUMRANGE,
            "postgresql_numrange_from_json",
            "postgresql_numrange_params",
            "postgresql_numrange_to_json",
        ],
        [
            POSTGRESQL_NUMMULTIRANGE,
            "postgresql_nummultirange_from_json",
            "postgresql_nummultirange_params",
            "postgresql_nummultirange_to_json",
        ],
        [
            POSTGRESQL_TSRANGE,
            "postgresql_tsrange_from_json",
            "postgresql_tsrange_params",
            "postgresql_tsrange_to_json",
        ],
        [
            POSTGRESQL_TSMULTIRANGE,
            "postgresql_tsmultirange_from_json",
            "postgresql_tsmultirange_params",
            "postgresql_tsmultirange_to_json",
        ],
        [
            POSTGRESQL_TSTZRANGE,
            "postgresql_tstzrange_from_json",
            "postgresql_tstzrange_params",
            "postgresql_tstzrange_to_json",
        ],
        [
            POSTGRESQL_TSTZMULTIRANGE,
            "postgresql_tstzmultirange_from_json",
            "postgresql_tstzmultirange_params",
            "postgresql_tstzmultirange_to_json",
        ],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert type_maps[type[0]] == TypeMap(
        from_json=type[1], params=type[2], to_json=type[3]
    )
