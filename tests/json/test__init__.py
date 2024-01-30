# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.json import JsonSerializer

from celery_sqlalchemy import errors

# system imports
from typing import Any

from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

# dependency imports
from pytest import raises

import orjson

PATH = "celery_sqlalchemy.json"


def test___init___set_json_key() -> None:
    serializer = JsonSerializer(json_key="test")

    assert serializer.json_key == "test"


def test___init___set_naive_utc_false() -> None:
    serializer = JsonSerializer(naive_utc=False)

    assert serializer.orjson_opts & orjson.OPT_NAIVE_UTC == 0


def test___init___set_naive_utc_true() -> None:
    serializer = JsonSerializer(naive_utc=True)

    assert serializer.orjson_opts & orjson.OPT_NAIVE_UTC == orjson.OPT_NAIVE_UTC


def test___init___set_passthrough_dataclass_false() -> None:
    serializer = JsonSerializer(passthrough_dataclass=False)

    assert serializer.orjson_opts & orjson.OPT_PASSTHROUGH_DATACLASS == 0


def test___init___set_passthrough_dataclass_true() -> None:
    serializer = JsonSerializer(passthrough_dataclass=True)

    assert (
        serializer.orjson_opts & orjson.OPT_PASSTHROUGH_DATACLASS
        == orjson.OPT_PASSTHROUGH_DATACLASS
    )


def test___init___set_on_deserialize_arg() -> None:
    deserialize_arg = Mock()
    serializer = JsonSerializer(on_deserialize_arg=deserialize_arg)

    assert serializer.deserialize_arg == deserialize_arg


def test___init___set_on_serialize_arg() -> None:
    serialize_arg = Mock()
    serializer = JsonSerializer(on_serialize_arg=serialize_arg)

    assert serializer.serialize_arg == serialize_arg


def test___init___set_utc_z_false() -> None:
    serializer = JsonSerializer(utc_z=False)

    assert serializer.orjson_opts & orjson.OPT_UTC_Z == 0


def test___init___set_utc_z_true() -> None:
    serializer = JsonSerializer(utc_z=True)

    assert serializer.orjson_opts & orjson.OPT_UTC_Z == orjson.OPT_UTC_Z


def test_arg_from_json__deserialize_arg() -> None:
    arg = Mock()
    deserialize_arg = Mock()
    serializer = JsonSerializer(on_deserialize_arg=deserialize_arg)

    assert serializer.arg_from_json(arg) == deserialize_arg.return_value

    deserialize_arg.assert_called_with(arg)


def test_arg_from_json__list() -> None:
    arg = [Mock()]
    serializer = JsonSerializer()

    result = serializer.arg_from_json(arg)

    assert result == arg
    assert id(result) != id(arg)


@patch(f"{PATH}.__name__")
@patch(f"{PATH}.sys")
@patch(f"{PATH}.schema_for_model_path")
def test_arg_from_json__model_class(
    schema_for_model_path: Mock, sys: Mock, __name__: Mock
) -> None:
    def ModelInit(self: Any, name: str) -> Any:
        self.name = name

    Model = type("Model", (object,), dict(name=None))
    Model.__init__ = ModelInit  # type: ignore

    field = Mock()
    field.name = "name"
    schema = Mock(fields=[field], model=Model)
    schema_for_model_path.return_value = schema
    model_path = Mock()
    name = Mock()
    arg = {
        "$model_path$": model_path,
        "name": name,
    }
    serializer = JsonSerializer()

    result = serializer.arg_from_json(arg)

    schema_for_model_path.assert_called_with(model_path, sys.modules[__name__])
    field.from_json.assert_called_with(field, name)

    assert result.name == field.from_json()


@patch(f"{PATH}.__name__")
@patch(f"{PATH}.sys")
@patch(f"{PATH}.schema_for_model_path")
def test_arg_from_json__model_instance(
    schema_for_model_path: Mock, sys: Mock, __name__: Mock
) -> None:
    class Model:
        def __init__(self, name: str):
            self.name = name

    field = Mock()
    field.name = "name"
    model = Model(name="test")
    schema = Mock(fields=[field], model=model)
    schema_for_model_path.return_value = schema
    model_path = Mock()
    name = Mock()
    arg = {
        "$model_path$": model_path,
        "name": name,
    }
    serializer = JsonSerializer()

    result = serializer.arg_from_json(arg)

    schema_for_model_path.assert_called_with(model_path, sys.modules[__name__])
    field.from_json.assert_called_with(field, name)

    assert isinstance(result, Model)
    assert id(result) != id(model)
    assert result.name == field.from_json()


def test_arg_from_json__other_than_model() -> None:
    arg = Mock()
    serializer = JsonSerializer()

    assert serializer.arg_from_json(arg) == arg


@patch(f"{PATH}.schema_map_key")
@patch(f"{PATH}.__name__")
@patch(f"{PATH}.sys")
@patch(f"{PATH}.inspect")
@patch(f"{PATH}.schema_for_model")
def test_arg_to_json__model(
    schema_for_model: Mock,
    inspect: Mock,
    sys: Mock,
    __name__: Mock,
    schema_map_key: Mock,
) -> None:
    instance_state = Mock()
    inspect.return_value = instance_state
    field = Mock()
    field.name = "name"
    schema = Mock(fields=[field])
    schema_for_model.return_value = schema
    arg = Mock(__table__=Mock())
    serializer = JsonSerializer()

    assert serializer.arg_to_json(arg) == {
        "$model_path$": schema_map_key.return_value,
        field.name: field.to_json.return_value,
    }

    inspect.assert_called_with(arg)
    schema_for_model.assert_called_with(arg, inspect().mapper, sys.modules[__name__])
    field.to_json.assert_called_with(field, arg.name)
    schema_map_key.assert_called_with(arg)


def test_arg_to_json__serialize_arg() -> None:
    arg = type("FakeType")
    serialize_arg = Mock()
    serializer = JsonSerializer(on_serialize_arg=serialize_arg)

    assert serializer.arg_to_json(arg) == serialize_arg.return_value

    serialize_arg.assert_called_with(arg)


def test_arg_to_json__set() -> None:
    serializer = JsonSerializer()

    assert serializer.arg_to_json({"test"}) == ["test"]


def test_arg_to_json__unserializable_with_table__raises_serialization_error() -> None:
    class Model:
        __table__ = "invalid"

    arg = Model()
    serializer = JsonSerializer()

    with raises(errors.SerializationError) as ex:
        assert serializer.arg_to_json(arg)

    assert str(ex.value) == f"Cannot serialize type '{arg.__class__.__name__}'"


def test_arg_to_json__unserializable_with_table__serialize_arg() -> None:
    class Model:
        __table__ = "invalid"

    arg = Model()
    serialize_arg = Mock()
    serializer = JsonSerializer(on_serialize_arg=serialize_arg)

    assert serializer.arg_to_json(arg) == serialize_arg.return_value

    serialize_arg.assert_called_with(arg)


def test_arg_to_json__unserializable_without_table__raises_serialization_error() -> (
    None
):
    arg = object()
    serializer = JsonSerializer()

    with raises(errors.SerializationError) as ex:
        assert serializer.arg_to_json(arg)

    assert str(ex.value) == f"Cannot serialize type '{arg.__class__.__name__}'"


@patch(f"{PATH}.orjson")
def test_message_from_args(orjson: Mock) -> None:
    args = Mock()
    serializer = JsonSerializer()

    assert serializer.message_from_args(args) == orjson.dumps.return_value

    orjson.dumps.assert_called_with(
        {
            "$arg$": args.arg,
            "$args$": args.args,
            "$kwargs$": args.kwargs,
        },
        default=serializer.arg_to_json,
        option=serializer.orjson_opts,
    )


@patch(f"{PATH}.JsonSerializer.arg_from_json")
@patch(f"{PATH}.orjson")
def test_message_to_args(orjson: Mock, arg_from_json: Mock) -> None:
    message = Mock()
    arg_value = Mock()
    kwarg_value = Mock()
    json = {
        "$arg$": arg_value,
        "$args$": [arg_value],
        "$kwargs$": {"name": kwarg_value},
    }
    orjson.loads.return_value = json
    serializer = JsonSerializer()

    args = serializer.message_to_args(message)

    orjson.loads.assert_called_with(message)

    assert arg_from_json.call_args_list == [
        call(arg_value),
        call(arg_value),
        call(kwarg_value),
    ]

    assert args.arg
    assert args.arg == arg_from_json()
    assert args.args
    assert args.args[0] == arg_from_json()
    assert args.kwargs
    assert args.kwargs["name"] == arg_from_json()
