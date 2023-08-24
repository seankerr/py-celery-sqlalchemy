# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy import json

# system imports
from typing import Any
from typing import Dict
from typing import List

from unittest.mock import MagicMock
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

    assert json.arg_from_json(arg) == schema.model.return_value

    schema_for_model_path.assert_called_with(model_path, sys.modules[__name__])
    field.from_json.assert_called_with(field, name)
    schema.model.assert_called_with(name=field.from_json())


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


def test_arg_to_json__other_than_model() -> None:
    arg: Dict[Any, Any] = {}

    assert json.arg_to_json(arg) == arg


def test_arg_to_json__other_than_model__instance_is_not_model() -> None:
    class InvalidModel:
        __table__ = "invalid"

    arg = InvalidModel()

    assert json.arg_to_json(arg) == arg


@patch(f"{PATH}.serialization")
@patch(f"{PATH}.message_from_args")
@patch(f"{PATH}.message_to_args")
def test_initialize(
    message_to_args: Mock, message_from_args: Mock, serialization: Mock
) -> None:
    celery = Mock()

    json.initialize(celery)

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
    assert orjson_opts == orjson.OPT_NAIVE_UTC


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


# --------------------------------------------------------------------------------------
# Standard serialization functions
# --------------------------------------------------------------------------------------


def test_array_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.array_from_json(field, value) == value


def test_array_params() -> None:
    column = Mock()

    assert not json.array_params(column)


def test_array_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.array_to_json(field, value) == value


def test_biginteger_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.biginteger_from_json(field, value) == value


def test_biginteger_params() -> None:
    column = Mock()

    assert not json.biginteger_params(column)


def test_biginteger_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.biginteger_to_json(field, value) == value


def test_boolean_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.boolean_from_json(field, value) == value


def test_boolean_params() -> None:
    column = Mock()

    assert not json.boolean_params(column)


def test_boolean_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.boolean_to_json(field, value) == value


@patch(f"{PATH}.date")
def test_date_from_json(date: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.date_from_json(field, value) == date.fromisoformat.return_value

    date.fromisoformat.assert_called_with(value)


def test_date_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.date_from_json(field, value) == value


def test_date_params() -> None:
    column = Mock()

    assert not json.date_params(column)


def test_date_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.date_to_json(field, value) == value


@patch(f"{PATH}.datetime")
def test_datetime_from_json(datetime: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.datetime_from_json(field, value) == datetime.fromisoformat.return_value

    datetime.fromisoformat.assert_called_with(value)


def test_datetime_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.datetime_from_json(field, value) == value


def test_datetime_params() -> None:
    column = Mock()

    assert not json.datetime_params(column)


def test_datetime_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.datetime_to_json(field, value) == value


@patch(f"{PATH}.numeric_from_json")
def test_double_from_json(numeric_from_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.double_from_json(field, value) == numeric_from_json.return_value

    numeric_from_json.assert_called_with(field, value)


def test_double_params() -> None:
    column = Mock()

    params = json.double_params(column)

    assert params.precision == column.type.precision
    assert params.scale is None
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.numeric_to_json")
def test_double_to_json(numeric_to_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.double_to_json(field, value) == numeric_to_json.return_value

    numeric_to_json.assert_called_with(field, value)


def test_enum_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.enum_from_json(field, value) == value


def test_enum_params() -> None:
    column = Mock()

    assert not json.enum_params(column)


def test_enum_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.enum_to_json(field, value) == value


@patch(f"{PATH}.numeric_from_json")
def test_float_from_json(numeric_from_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.float_from_json(field, value) == numeric_from_json.return_value

    numeric_from_json.assert_called_with(field, value)


def test_float_params() -> None:
    column = Mock()

    params = json.float_params(column)

    assert params.precision == column.type.precision
    assert params.scale is None
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.numeric_to_json")
def test_float_to_json(numeric_to_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.float_to_json(field, value) == numeric_to_json.return_value

    numeric_to_json.assert_called_with(field, value)


def test_integer_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.integer_from_json(field, value) == value


def test_integer_params() -> None:
    column = Mock()

    assert not json.integer_params(column)


def test_integer_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.integer_to_json(field, value) == value


@patch(f"{PATH}.timedelta")
def test_interval_from_json(timedelta: Mock) -> None:
    field = Mock()
    value = MagicMock()

    assert json.interval_from_json(field, value) == timedelta.return_value

    timedelta.assert_called_with(
        hours=value[0], seconds=value[1], microseconds=value[2]
    )


def test_interval_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.interval_from_json(field, value) == value


def test_interval_params() -> None:
    column = Mock()

    assert not json.interval_params(column)


def test_interval_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.interval_to_json(field, value) == [
        value.days,
        value.seconds,
        value.microseconds,
    ]


def test_interval_to_json__none() -> None:
    field = Mock()
    value = None

    assert json.interval_to_json(field, value) == value


def test_largebinary_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.largebinary_from_json(field, value) == value


def test_largebinary_params() -> None:
    column = Mock()

    assert not json.largebinary_params(column)


def test_largebinary_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.largebinary_to_json(field, value) == value


def test_json_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.json_from_json(field, value) == value


def test_json_params() -> None:
    column = Mock()

    assert not json.json_params(column)


def test_json_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.json_to_json(field, value) == value


@patch(f"{PATH}.Decimal")
def test_numeric_from_json__decimal(Decimal: Mock) -> None:
    field = Mock(params=json.NumericParams(None, None, None, True))
    value = Mock()

    assert json.numeric_from_json(field, value) == Decimal.return_value

    Decimal.assert_called_with(value)


def test_numeric_from_json__float() -> None:
    field = Mock(params=json.NumericParams(None, None, None, False))
    value = Mock()

    assert json.numeric_from_json(field, value) == value


def test_numeric_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.numeric_from_json(field, value) == value


def test_numeric_params() -> None:
    column = Mock()

    params = json.numeric_params(column)

    assert params.precision == column.type.precision
    assert params.scale == column.type.scale
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.round")
def test_numeric_to_json__decimal(round: Mock) -> None:
    field = Mock(params=json.NumericParams(None, None, None, True))
    value = Mock()

    assert json.numeric_to_json(field, value) == str(round.return_value)

    round.assert_called_with(value, field.params.scale)


def test_numeric_to_json__float() -> None:
    field = Mock(params=json.NumericParams(None, None, None, False))
    value = Mock()

    assert json.numeric_to_json(field, value) == value


def test_numeric_to_json__none() -> None:
    field = Mock()
    value = None

    assert json.numeric_to_json(field, value) == value


def test_smallinteger_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.smallinteger_from_json(field, value) == value


def test_smallinteger_params() -> None:
    column = Mock()

    assert not json.smallinteger_params(column)


def test_smallinteger_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.smallinteger_to_json(field, value) == value


def test_string_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.string_from_json(field, value) == value


def test_string_params() -> None:
    column = Mock()

    assert not json.string_params(column)


def test_string_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.string_to_json(field, value) == value


def test_text_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.text_from_json(field, value) == value


def test_text_params() -> None:
    column = Mock()

    assert not json.text_params(column)


def test_text_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.text_to_json(field, value) == value


@patch(f"{PATH}.time")
def test_time_from_json(time: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.time_from_json(field, value) == time.fromisoformat.return_value

    time.fromisoformat.assert_called_with(value)


def test_time_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.time_from_json(field, value) == value


def test_time_params() -> None:
    column = Mock()

    assert not json.time_params(column)


def test_time_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.time_to_json(field, value) == value


def test_unicode_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.unicode_from_json(field, value) == value


def test_unicode_params() -> None:
    column = Mock()

    assert not json.unicode_params(column)


def test_unicode_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.unicode_to_json(field, value) == value


def test_unicodetext_from_json() -> None:
    field = Mock()
    value = Mock()

    assert json.unicodetext_from_json(field, value) == value


def test_unicodetext_params() -> None:
    column = Mock()

    assert not json.unicodetext_params(column)


def test_unicodetext_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.unicodetext_to_json(field, value) == value


@patch(f"{PATH}.UUID")
def test_uuid_from_json(UUID: Mock) -> None:
    field = Mock()
    value = Mock()

    assert json.uuid_from_json(field, value) == UUID.return_value

    UUID.assert_called_with(value)


def test_uuid_from_json__none() -> None:
    field = Mock()
    value = None

    assert json.uuid_from_json(field, value) == value


def test_uuid_params() -> None:
    column = Mock()

    assert not json.uuid_params(column)


def test_uuid_to_json() -> None:
    field = Mock()
    value = Mock()

    assert json.uuid_to_json(field, value) == value
