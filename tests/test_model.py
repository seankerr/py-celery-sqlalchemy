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

from sqlalchemy.dialects.postgresql.array import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql.named_types import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql.hstore import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql.json import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql.json import JSONB as POSTGRESQL_JSONB

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

    params = Mock()
    value_in = Mock()
    value_out = Mock()

    setattr(format_module, type_maps[type].params, params)
    setattr(format_module, type_maps[type].value_in, value_in)
    setattr(format_module, type_maps[type].value_out, value_out)

    schema = map_model(model, mapper, format_module)

    params.assert_called_with(column.type)

    assert schema.fields == [
        Field(
            name=column.name,
            params=params(),
            type=type,
            value_in=value_in,
            value_out=value_out,
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
        [sqltypes.ARRAY, "array_params", "array_in", "array_out"],
        [
            sqltypes.BigInteger,
            "big_integer_params",
            "big_integer_in",
            "big_integer_out",
        ],
        [sqltypes.Boolean, "boolean_params", "boolean_in", "boolean_out"],
        [sqltypes.Date, "date_params", "date_in", "date_out"],
        [sqltypes.DateTime, "date_time_params", "date_time_in", "date_time_out"],
        [sqltypes.Double, "double_params", "double_in", "double_out"],
        [sqltypes.Enum, "enum_params", "enum_in", "enum_out"],
        [sqltypes.Float, "float_params", "float_in", "float_out"],
        [sqltypes.Integer, "integer_params", "integer_in", "integer_out"],
        [sqltypes.Interval, "interval_params", "interval_in", "interval_out"],
        [
            sqltypes.LargeBinary,
            "large_binary_params",
            "large_binary_in",
            "large_binary_out",
        ],
        [sqltypes.JSON, "json_params", "json_in", "json_out"],
        [sqltypes.Numeric, "numeric_params", "numeric_in", "numeric_out"],
        [
            sqltypes.SmallInteger,
            "small_integer_params",
            "small_integer_in",
            "small_integer_out",
        ],
        [sqltypes.String, "string_params", "string_in", "string_out"],
        [sqltypes.Text, "text_params", "text_in", "text_out"],
        [sqltypes.Time, "time_params", "time_in", "time_out"],
        [sqltypes.Unicode, "unicode_params", "unicode_in", "unicode_out"],
        [
            sqltypes.UnicodeText,
            "unicode_text_params",
            "unicode_text_in",
            "unicode_text_out",
        ],
        [sqltypes.UUID, "uuid_params", "uuid_in", "uuid_out"],
        [
            POSTGRESQL_ARRAY,
            "postgresql_array_params",
            "postgresql_array_in",
            "postgresql_array_out",
        ],
        [
            POSTGRESQL_ENUM,
            "postgresql_enum_params",
            "postgresql_enum_in",
            "postgresql_enum_out",
        ],
        [
            POSTGRESQL_HSTORE,
            "postgresql_hstore_params",
            "postgresql_hstore_in",
            "postgresql_hstore_out",
        ],
        [
            POSTGRESQL_JSON,
            "postgresql_json_params",
            "postgresql_json_in",
            "postgresql_json_out",
        ],
        [
            POSTGRESQL_JSONB,
            "postgresql_jsonb_params",
            "postgresql_jsonb_in",
            "postgresql_jsonb_out",
        ],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert type_maps[type[0]] == TypeMap(
        params=type[1], value_in=type[2], value_out=type[3]
    )
