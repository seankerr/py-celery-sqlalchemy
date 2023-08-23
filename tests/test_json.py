# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.json import arg_from_json
from celery_sqlalchemy.json import arg_to_json
from celery_sqlalchemy.json import initialize
from celery_sqlalchemy.json import message_from_args
from celery_sqlalchemy.json import message_to_args

# system imports
from typing import Any
from typing import Dict
from typing import List

from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

# dependency imports
import orjson

PATH = "celery_sqlalchemy.json"


@patch(f"{PATH}.__name__")
@patch(f"{PATH}.sys")
@patch(f"{PATH}.schema_for_model_path")
def test_arg_from_json__model(
    schema_for_model_path: Mock, sys: Mock, __name__: Mock
) -> None:
    field = Mock()
    field.name = "name"
    schema = Mock(fields=[field])
    schema_for_model_path.return_value = schema
    model_path = Mock()
    name = Mock()
    arg = {
        "$model_path$": model_path,
        "name": name,
    }

    assert arg_from_json(arg) == schema.model.return_value

    schema_for_model_path.assert_called_with(model_path, sys.modules[__name__])
    field.value_in.assert_called_with(name)
    schema.model.assert_called_with(name=field.value_in())


def test_arg_from_json__other_than_model() -> None:
    arg = Mock()

    assert arg_from_json(arg) == arg


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

    assert arg_to_json(arg) == {
        "$model_path$": schema_map_key.return_value,
        field.name: field.value_out.return_value,
    }

    inspect.assert_called_with(arg)
    schema_for_model.assert_called_with(arg, inspect().mapper, sys.modules[__name__])
    field.value_out.assert_called_with(arg.name)
    schema_map_key.assert_called_with(arg)


def test_arg_to_json__other_than_model() -> None:
    arg: Dict[Any, Any] = {}

    assert arg_to_json(arg) == arg


def test_arg_to_json__other_than_model__instance_is_not_model() -> None:
    class InvalidModel:
        __table__ = "invalid"

    arg = InvalidModel()

    assert arg_to_json(arg) == arg


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    initialize(celery)

    assert celery.conf.accept_content == ["json+sqlalchemy"]
    assert celery.conf.result_accept_content == ["json+sqlalchemy"]
    assert celery.conf.task_serializer == "json+sqlalchemy"

    serialization.register.assert_called_with(
        "json+sqlalchemy",
        message_from_args,
        message_to_args,
        "json",
    )

    from celery_sqlalchemy.json import json_module_key
    from celery_sqlalchemy.json import orjson_opts

    assert json_module_key == "$model_path$"
    assert orjson_opts == orjson.OPT_NAIVE_UTC | orjson.OPT_UTC_Z


@patch(f"{PATH}.orjson")
@patch(f"{PATH}.orjson_opts")
def test_message_from_args(orjson_opts: Mock, orjson: Mock) -> None:
    args = Mock()

    assert message_from_args(args) == orjson.dumps.return_value

    orjson.dumps.assert_called_with(args, default=arg_to_json, option=orjson_opts)


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

    assert message_to_args(message) == orjson.loads.return_value

    orjson.loads.assert_called_with(message)

    assert arg_from_json.call_args_list == [call(arg_value), call(kwarg_value)]

    assert data[0][0] == arg_from_json()
    assert data[1]["name"] == arg_from_json()


@patch(f"{PATH}.orjson")
def test_message_to_args__celery_message(orjson: Mock) -> None:
    message = Mock()

    assert message_to_args(message) == orjson.loads.return_value
