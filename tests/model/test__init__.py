# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import postgresql_1_4
from celery_sqlalchemy.model import postgresql_2_0
from celery_sqlalchemy.model import sqlalchemy_1_4
from celery_sqlalchemy.model import sqlalchemy_2_0

from celery_sqlalchemy.model import add_schema
from celery_sqlalchemy.model import load_model
from celery_sqlalchemy.model import map_model
from celery_sqlalchemy.model import schema_for_model
from celery_sqlalchemy.model import schema_for_model_path
from celery_sqlalchemy.model import schema_map_key
from celery_sqlalchemy.model import type_maps

from celery_sqlalchemy.schema import Field

# system imports
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

# dependency imports
from pytest import mark

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


def test_type_maps() -> None:
    assert type_maps == {
        **sqlalchemy_1_4.type_maps,
        **sqlalchemy_2_0.type_maps,
        **postgresql_1_4.type_maps,
        **postgresql_2_0.type_maps,
    }
