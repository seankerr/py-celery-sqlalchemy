# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy import errors
from celery_sqlalchemy import json

# system imports
from typing import Any
from typing import List

from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

# dependency imports
from pytest import raises

import orjson

PATH = "celery_sqlalchemy.json"


@patch(f"{PATH}.deserialize_arg")
def test_arg_from_json__deserialize_arg(deserialize_arg: Mock) -> None:
    arg = Mock()

    assert json.arg_from_json(arg) == deserialize_arg.return_value

    deserialize_arg.assert_called_with(arg)


def test_arg_from_json__list() -> None:
    arg = [Mock()]

    result = json.arg_from_json(arg)

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

    result = json.arg_from_json(arg)

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

    result = json.arg_from_json(arg)

    schema_for_model_path.assert_called_with(model_path, sys.modules[__name__])
    field.from_json.assert_called_with(field, name)

    assert isinstance(result, Model)
    assert id(result) != id(model)
    assert result.name == field.from_json()


def test_arg_from_json__other_than_model() -> None:
    arg = Mock()

    assert json.arg_from_json(arg) == arg


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

    assert json.arg_to_json(arg) == {
        "$model_path$": schema_map_key.return_value,
        field.name: field.to_json.return_value,
    }

    inspect.assert_called_with(arg)
    schema_for_model.assert_called_with(arg, inspect().mapper, sys.modules[__name__])
    field.to_json.assert_called_with(field, arg.name)
    schema_map_key.assert_called_with(arg)


@patch(f"{PATH}.serialize_arg")
def test_arg_to_json__serialize_arg(serialize_arg: Mock) -> None:
    arg = type("FakeType")

    assert json.arg_to_json(arg) == serialize_arg.return_value

    serialize_arg.assert_called_with(arg)


def test_arg_to_json__set() -> None:
    assert json.arg_to_json({"test"}) == ["test"]


def test_arg_to_json__unserializable_with_table__raises_serialization_error() -> None:
    class Model:
        __table__ = "invalid"

    arg = Model()

    with raises(errors.SerializationError) as ex:
        assert json.arg_to_json(arg)

    assert str(ex.value) == f"Cannot serialize type '{arg.__class__.__name__}'"


@patch(f"{PATH}.serialize_arg")
def test_arg_to_json__unserializable_with_table__serialize_arg(
    serialize_arg: Mock,
) -> None:
    class Model:
        __table__ = "invalid"

    arg = Model()

    assert json.arg_to_json(arg) == serialize_arg.return_value

    serialize_arg.assert_called_with(arg)


def test_arg_to_json__unserializable_without_table__raises_serialization_error() -> (
    None
):
    arg = object()

    with raises(errors.SerializationError) as ex:
        assert json.arg_to_json(arg)

    assert str(ex.value) == f"Cannot serialize type '{arg.__class__.__name__}'"


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery)

    serialization.register.assert_called_with(
        "json+sqlalchemy",
        message_from_args,
        message_to_args,
        "json",
    )

    assert celery.conf.accept_content == ["json+sqlalchemy"]
    assert celery.conf.result_accept_content == ["json+sqlalchemy"]
    assert celery.conf.task_serializer == "json+sqlalchemy"

    from celery_sqlalchemy.json import deserialize_arg
    from celery_sqlalchemy.json import json_module_key
    from celery_sqlalchemy.json import orjson_opts
    from celery_sqlalchemy.json import serialize_arg

    assert not deserialize_arg
    assert json_module_key == "$model_path$"
    assert orjson_opts & orjson.OPT_NAIVE_UTC == orjson.OPT_NAIVE_UTC
    assert orjson_opts & orjson.OPT_UTC_Z == 0
    assert not serialize_arg


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_apply_serializer(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery, apply_serializer=False)

    assert isinstance(celery.conf.accept_content, Mock)
    assert isinstance(celery.conf.result_accept_content, Mock)
    assert isinstance(celery.conf.task_serializer, Mock)


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_content_type(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery, content_type="test")

    serialization.register.assert_called_with(
        "test",
        message_from_args,
        message_to_args,
        "json",
    )

    assert celery.conf.accept_content == ["test"]
    assert celery.conf.result_accept_content == ["test"]
    assert celery.conf.task_serializer == "test"


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_json_key(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery, json_key="test")

    from celery_sqlalchemy.json import json_module_key

    assert json_module_key == "test"


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_naive_utc_false(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, naive_utc=False)

    assert json.orjson_opts & orjson.OPT_NAIVE_UTC == 0


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_naive_utc_true(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, naive_utc=True)

    assert json.orjson_opts & orjson.OPT_NAIVE_UTC == orjson.OPT_NAIVE_UTC


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_passthrough_dataclass_false(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, passthrough_dataclass=False)

    assert json.orjson_opts & orjson.OPT_PASSTHROUGH_DATACLASS == 0


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_passthrough_dataclass_true(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, passthrough_dataclass=True)

    assert (
        json.orjson_opts & orjson.OPT_PASSTHROUGH_DATACLASS
        == orjson.OPT_PASSTHROUGH_DATACLASS
    )


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_on_deserialize_arg(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery, on_deserialize_arg=lambda x: x)

    from celery_sqlalchemy.json import deserialize_arg

    assert deserialize_arg


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_on_serialize_arg(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery, on_serialize_arg=lambda x: x)

    from celery_sqlalchemy.json import serialize_arg

    assert serialize_arg


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_utc_z_false(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, utc_z=False)

    assert json.orjson_opts & orjson.OPT_UTC_Z == 0


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize__set_utc_z_true(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.orjson_opts = 0

    json.initialize(celery, utc_z=True)

    assert json.orjson_opts & orjson.OPT_UTC_Z == orjson.OPT_UTC_Z


@patch(f"{PATH}.orjson")
@patch(f"{PATH}.orjson_opts")
def test_message_from_args(orjson_opts: Mock, orjson: Mock) -> None:
    args = Mock()

    assert json.message_from_args(args) == orjson.dumps.return_value

    orjson.dumps.assert_called_with(args, default=json.arg_to_json, option=orjson_opts)


@patch(f"{PATH}.arg_from_json")
@patch(f"{PATH}.orjson")
def test_message_to_args(orjson: Mock, arg_from_json: Mock) -> None:
    message = Mock()
    arg_value = Mock()
    kwarg_value = Mock()
    data: List[Any] = [
        [arg_value],
        {"name": kwarg_value},
    ]
    orjson.loads.return_value = data

    assert json.message_to_args(message) == orjson.loads.return_value

    orjson.loads.assert_called_with(message)

    assert arg_from_json.call_args_list == [call(arg_value), call(kwarg_value)]

    assert data[0][0] == arg_from_json()
    assert data[1]["name"] == arg_from_json()


@patch(f"{PATH}.enumerate")
@patch(f"{PATH}.orjson")
def test_message_to_args__celery_message(orjson: Mock, enumerate: Mock) -> None:
    enumerate.side_effect = KeyError()
    message = Mock()

    assert json.message_to_args(message) == orjson.loads.return_value
