# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.celery import deserialize
from celery_sqlalchemy.celery import initialize
from celery_sqlalchemy.celery import serialize

from celery_sqlalchemy import errors

# system imports
from typing import Any
from typing import Dict

from unittest.mock import Mock
from unittest.mock import patch

# dependency imports
from pytest import mark
from pytest import raises

PATH = "celery_sqlalchemy.celery"


@patch(f"{PATH}.serialization")
def test___init__(serialization: Mock) -> None:
    celery = Mock()
    serializer = Mock()
    content_type = "json+sqlalchemy"

    initialize(celery, serializer)

    serialization.register.assert_called_with(
        content_type,
        serialize,
        deserialize,
        "json",
    )

    assert celery.conf.accept_content == [content_type]
    assert celery.conf.result_accept_content == [content_type]
    assert celery.conf.task_serializer == content_type

    from celery_sqlalchemy.celery import __SERIALIZER__

    assert serializer == __SERIALIZER__


@patch(f"{PATH}.serialization")
def test___init___set_apply_serializer__false(serialization: Mock) -> None:
    celery = Mock()
    serializer = Mock()

    celery.conf.accept_content = None
    celery.conf.result_accept_content = None
    celery.conf.task_serializer = None

    initialize(celery, serializer, apply_serializer=False)

    serialization.register.assert_called_with(
        "json+sqlalchemy",
        serialize,
        deserialize,
        "json",
    )

    assert not celery.conf.accept_content
    assert not celery.conf.result_accept_content
    assert not celery.conf.task_serializer


@patch(f"{PATH}.serialization")
def test___init___set_apply_serializer__true(serialization: Mock) -> None:
    celery = Mock()
    serializer = Mock()
    content_type = "json+sqlalchemy"

    celery.conf.accept_content = None
    celery.conf.result_accept_content = None
    celery.conf.task_serializer = None

    initialize(celery, serializer, apply_serializer=True)

    serialization.register.assert_called_with(
        content_type,
        serialize,
        deserialize,
        "json",
    )

    assert celery.conf.accept_content == [content_type]
    assert celery.conf.result_accept_content == [content_type]
    assert celery.conf.task_serializer == content_type


@patch(f"{PATH}.serialization")
def test___init___set_content_type(serialization: Mock) -> None:
    celery = Mock()
    serializer = Mock()
    content_type = Mock()

    initialize(celery, serializer, content_type=content_type)

    serialization.register.assert_called_with(
        content_type,
        serialize,
        deserialize,
        "json",
    )

    assert celery.conf.accept_content == [content_type]
    assert celery.conf.result_accept_content == [content_type]
    assert celery.conf.task_serializer == content_type


def test_deserialize() -> None:
    serializer = Mock()

    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = serializer

    args = Mock()
    message = Mock()
    serializer.message_to_args.return_value = args

    assert deserialize(message) == [args.args, args.kwargs, args.arg]

    serializer.message_to_args.assert_called_with(message)


@mark.parametrize("ex", [KeyError(), TypeError()])
@patch(f"{PATH}.orjson")
def test_deserialize__celery_message(orjson: Mock, ex: Exception) -> None:
    serializer = Mock()
    serializer.message_to_args.side_effect = ex

    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = serializer

    message = Mock()

    assert deserialize(message) == orjson.loads.return_value

    serializer.message_to_args.assert_called_with(message)
    orjson.loads.assert_called_with(message)


def test_deserialize__raises_serialization_error() -> None:
    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = None

    with raises(errors.SerializationError) as ex:
        deserialize(Mock())

    assert str(ex.value) == "Serializer has not been initialized"


@patch(f"{PATH}.orjson")
def test_serialize__dict(orjson: Mock) -> None:
    serializer = Mock()

    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = serializer

    args: Dict[str, Any] = dict()

    serialize(args)

    orjson.dumps.assert_called_with(args)


def test_serialize__raises_serialization_error() -> None:
    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = None

    with raises(errors.SerializationError) as ex:
        serialize(Mock())

    assert str(ex.value) == "Serializer has not been initialized"


@patch(f"{PATH}.Args")
def test_serialize__tuple(Args: Mock) -> None:
    serializer = Mock()

    from celery_sqlalchemy import celery

    celery.__SERIALIZER__ = serializer

    args = (Mock(), Mock(), Mock())

    serialize(args)

    Args.assert_called_with(arg=args[2], args=args[0], kwargs=args[1])
    serializer.message_from_args.assert_called_with(Args())
