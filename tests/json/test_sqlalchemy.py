# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.json import sqlalchemy

# system imports
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

PATH = "celery_sqlalchemy.json.sqlalchemy"


def test_array_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.array_from_json(field, value) == value


def test_array_params() -> None:
    column = Mock()

    assert not sqlalchemy.array_params(column)


def test_array_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.array_to_json(field, value) == value


def test_biginteger_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.biginteger_from_json(field, value) == value


def test_biginteger_params() -> None:
    column = Mock()

    assert not sqlalchemy.biginteger_params(column)


def test_biginteger_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.biginteger_to_json(field, value) == value


def test_boolean_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.boolean_from_json(field, value) == value


def test_boolean_params() -> None:
    column = Mock()

    assert not sqlalchemy.boolean_params(column)


def test_boolean_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.boolean_to_json(field, value) == value


@patch(f"{PATH}.date")
def test_date_from_json(date: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.date_from_json(field, value) == date.fromisoformat.return_value

    date.fromisoformat.assert_called_with(value)


def test_date_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.date_from_json(field, value) == value


def test_date_params() -> None:
    column = Mock()

    assert not sqlalchemy.date_params(column)


def test_date_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.date_to_json(field, value) == value


@patch(f"{PATH}.datetime")
def test_datetime_from_json(datetime: Mock) -> None:
    field = Mock()
    value = Mock()

    assert (
        sqlalchemy.datetime_from_json(field, value)
        == datetime.fromisoformat.return_value
    )

    datetime.fromisoformat.assert_called_with(value)


def test_datetime_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.datetime_from_json(field, value) == value


def test_datetime_params() -> None:
    column = Mock()

    assert not sqlalchemy.datetime_params(column)


def test_datetime_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.datetime_to_json(field, value) == value


@patch(f"{PATH}.numeric_from_json")
def test_double_from_json(numeric_from_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.double_from_json(field, value) == numeric_from_json.return_value

    numeric_from_json.assert_called_with(field, value)


def test_double_params() -> None:
    column = Mock()

    params = sqlalchemy.double_params(column)

    assert params.precision == column.type.precision
    assert params.scale is None
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.numeric_to_json")
def test_double_to_json(numeric_to_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.double_to_json(field, value) == numeric_to_json.return_value

    numeric_to_json.assert_called_with(field, value)


def test_enum_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.enum_from_json(field, value) == value


def test_enum_params() -> None:
    column = Mock()

    assert not sqlalchemy.enum_params(column)


def test_enum_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.enum_to_json(field, value) == value


@patch(f"{PATH}.numeric_from_json")
def test_float_from_json(numeric_from_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.float_from_json(field, value) == numeric_from_json.return_value

    numeric_from_json.assert_called_with(field, value)


def test_float_params() -> None:
    column = Mock()

    params = sqlalchemy.float_params(column)

    assert params.precision == column.type.precision
    assert params.scale is None
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.numeric_to_json")
def test_float_to_json(numeric_to_json: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.float_to_json(field, value) == numeric_to_json.return_value

    numeric_to_json.assert_called_with(field, value)


def test_integer_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.integer_from_json(field, value) == value


def test_integer_params() -> None:
    column = Mock()

    assert not sqlalchemy.integer_params(column)


def test_integer_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.integer_to_json(field, value) == value


@patch(f"{PATH}.timedelta")
def test_interval_from_json(timedelta: Mock) -> None:
    field = Mock()
    value = MagicMock()

    assert sqlalchemy.interval_from_json(field, value) == timedelta.return_value

    timedelta.assert_called_with(
        hours=value[0], seconds=value[1], microseconds=value[2]
    )


def test_interval_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.interval_from_json(field, value) == value


def test_interval_params() -> None:
    column = Mock()

    assert not sqlalchemy.interval_params(column)


def test_interval_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.interval_to_json(field, value) == [
        value.days,
        value.seconds,
        value.microseconds,
    ]


def test_interval_to_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.interval_to_json(field, value) == value


def test_largebinary_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.largebinary_from_json(field, value) == value


def test_largebinary_params() -> None:
    column = Mock()

    assert not sqlalchemy.largebinary_params(column)


def test_largebinary_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.largebinary_to_json(field, value) == value


def test_json_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.json_from_json(field, value) == value


def test_json_params() -> None:
    column = Mock()

    assert not sqlalchemy.json_params(column)


def test_json_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.json_to_json(field, value) == value


@patch(f"{PATH}.Decimal")
def test_numeric_from_json__decimal(Decimal: Mock) -> None:
    field = Mock(params=sqlalchemy.NumericParams(None, None, None, True))
    value = Mock()

    assert sqlalchemy.numeric_from_json(field, value) == Decimal.return_value

    Decimal.assert_called_with(value)


def test_numeric_from_json__float() -> None:
    field = Mock(params=sqlalchemy.NumericParams(None, None, None, False))
    value = Mock()

    assert sqlalchemy.numeric_from_json(field, value) == value


def test_numeric_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.numeric_from_json(field, value) == value


def test_numeric_params() -> None:
    column = Mock()

    params = sqlalchemy.numeric_params(column)

    assert params.precision == column.type.precision
    assert params.scale == column.type.scale
    assert params.decimal_return_scale == column.type.decimal_return_scale
    assert params.asdecimal == column.type.asdecimal


@patch(f"{PATH}.round")
def test_numeric_to_json__decimal(round: Mock) -> None:
    field = Mock(params=sqlalchemy.NumericParams(None, None, None, True))
    value = Mock()

    assert sqlalchemy.numeric_to_json(field, value) == str(round.return_value)

    round.assert_called_with(value, field.params.scale)


def test_numeric_to_json__float() -> None:
    field = Mock(params=sqlalchemy.NumericParams(None, None, None, False))
    value = Mock()

    assert sqlalchemy.numeric_to_json(field, value) == value


def test_numeric_to_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.numeric_to_json(field, value) == value


def test_smallinteger_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.smallinteger_from_json(field, value) == value


def test_smallinteger_params() -> None:
    column = Mock()

    assert not sqlalchemy.smallinteger_params(column)


def test_smallinteger_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.smallinteger_to_json(field, value) == value


def test_string_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.string_from_json(field, value) == value


def test_string_params() -> None:
    column = Mock()

    assert not sqlalchemy.string_params(column)


def test_string_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.string_to_json(field, value) == value


def test_text_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.text_from_json(field, value) == value


def test_text_params() -> None:
    column = Mock()

    assert not sqlalchemy.text_params(column)


def test_text_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.text_to_json(field, value) == value


@patch(f"{PATH}.time")
def test_time_from_json(time: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.time_from_json(field, value) == time.fromisoformat.return_value

    time.fromisoformat.assert_called_with(value)


def test_time_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.time_from_json(field, value) == value


def test_time_params() -> None:
    column = Mock()

    assert not sqlalchemy.time_params(column)


def test_time_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.time_to_json(field, value) == value


def test_unicode_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.unicode_from_json(field, value) == value


def test_unicode_params() -> None:
    column = Mock()

    assert not sqlalchemy.unicode_params(column)


def test_unicode_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.unicode_to_json(field, value) == value


def test_unicodetext_from_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.unicodetext_from_json(field, value) == value


def test_unicodetext_params() -> None:
    column = Mock()

    assert not sqlalchemy.unicodetext_params(column)


def test_unicodetext_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.unicodetext_to_json(field, value) == value


@patch(f"{PATH}.UUID")
def test_uuid_from_json(UUID: Mock) -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.uuid_from_json(field, value) == UUID.return_value

    UUID.assert_called_with(value)


def test_uuid_from_json__none() -> None:
    field = Mock()
    value = None

    assert sqlalchemy.uuid_from_json(field, value) == value


def test_uuid_params() -> None:
    column = Mock()

    assert not sqlalchemy.uuid_params(column)


def test_uuid_to_json() -> None:
    field = Mock()
    value = Mock()

    assert sqlalchemy.uuid_to_json(field, value) == value
