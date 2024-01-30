# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .types import Args
from .types import Message
from .types import Serializer

from . import errors

# system imports
from typing import Any
from typing import List
from typing import Optional
from typing import Union

# dependency imports
from celery import Celery

from kombu import serialization

__SERIALIZER__: Optional[Serializer] = None


def initialize(
    celery: Celery,
    serializer: Serializer,
    content_type: str = "json+sqlalchemy",
) -> None:
    """
    Initialize the celery module.

    Parameters:
        celery (Celery): Celery instance.
        serializer (Serializer): Serializer instance.
        content_type (str): The content type to use for this serializer.
    """
    global __SERIALIZER__

    serialization.register(
        content_type,
        message_from_args,
        message_to_args,
        "json",
    )

    celery.conf.accept_content = [content_type]
    celery.conf.result_accept_content = [content_type]
    celery.conf.task_serializer = content_type

    __SERIALIZER__ = serializer


def message_from_args(args: Union[List[Any], str]) -> Union[Message, str]:
    """
    Serialize arguments into their Celery message equivalent.

    Parameters:
        args (dict | list | Any): Task arguments.
    """
    if not __SERIALIZER__:
        raise errors.SerializationError("Serializer has not been initialized")

    if isinstance(args, list):
        return __SERIALIZER__.message_from_args(
            Args(arg=None, args=args[0], kwargs=args[1])
        )

    else:
        return __SERIALIZER__.message_from_args(Args(arg=args, args=[], kwargs={}))


def message_to_args(message: Message) -> Union[List[Any], str]:
    """
    Deserialize a Celery message into its python equivalent.

    Parameters:
        message (Message): Message.
    """
    if not __SERIALIZER__:
        raise errors.SerializationError("Serializer has not been initialized")

    args = __SERIALIZER__.message_to_args(message)

    if args.arg:
        return args.arg

    else:
        return [args.args, args.kwargs]
