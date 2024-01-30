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
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

# dependency imports
from celery import Celery

from kombu import serialization

import orjson

__SERIALIZER__: Optional[Serializer] = None


def initialize(
    celery: Celery,
    serializer: Serializer,
    apply_serializer: bool = True,
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
        serialize,
        deserialize,
        "json",
    )

    if apply_serializer:
        celery.conf.accept_content = [content_type]
        celery.conf.result_accept_content = [content_type]
        celery.conf.task_serializer = content_type

    __SERIALIZER__ = serializer


def deserialize(message: Message) -> Union[List[Any], str]:
    """
    Deserialize a Celery message into its python equivalent.

    Parameters:
        message (Message): Message.
    """
    if not __SERIALIZER__:
        raise errors.SerializationError("Serializer has not been initialized")

    try:
        args = __SERIALIZER__.message_to_args(message)

        return [args.args, args.kwargs, args.arg]

    except (KeyError, TypeError):
        # celery message
        return orjson.loads(message)


def serialize(
    args: Union[Dict[str, Any], Tuple[List[Any], Dict[str, Any], Any]]
) -> Message:
    """
    Serialize arguments into their Celery message equivalent.

    Parameters:
        args (dict | tuple): Task arguments.
    """
    if not __SERIALIZER__:
        raise errors.SerializationError("Serializer has not been initialized")

    if isinstance(args, tuple):
        # task
        return __SERIALIZER__.message_from_args(
            Args(arg=args[2], args=args[0], kwargs=args[1])
        )

    else:
        # celery message
        return orjson.dumps(args)
