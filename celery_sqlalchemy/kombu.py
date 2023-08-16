# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# system imports
from typing import Any
from typing import Dict
from typing import List

# dependency imports
from celery import Celery

from kombu import serialization


def initialize(celery: Celery) -> None:
    """
    Initialize kombu with our custom serialization functions.

    Parameters:
        celery (Celery): Celery instance.
    """
    serialization.register(
        "custom_json", kombu_dict_to_message, kombu_message_to_dict, "json"
    )


def kombu_arg_to_any(models: Any, arg: Any) -> Any:
    """
    Convert a arg into its model equivalent.

    :param module: Models module.
    :param object: Any argument value.
    """
    try:
        model_class = getattr(models, arg["__model__"])

    except (KeyError, TypeError):
        if isinstance(arg, list):
            return [kombu_arg_to_any(models, value) for value in arg]

        return arg

    return model_class.from_event(arg)


def kombu_dict_to_message(data: Dict[str, Any]) -> str:
    """
    Convert a dict into its message equivalent.

    :param dict: Dict.
    """
    return dumps(data, default=serialize_to_json)


def kombu_message_to_dict(message: bytes | str) -> Dict[str, Any]:
    """
    Convert a message into its dict equivalent.

    :param str: Message.
    """
    models = proxy.connect(proxy.MODELS)

    # convert arguments back into their model equivalent
    data = loads(message)

    try:
        args = data[0]
        kwargs = data[1]

        for arg_n, arg_v in enumerate(args):
            args[arg_n] = kombu_arg_to_any(models, arg_v)

        for arg_k in kwargs.keys():
            kwargs[arg_k] = kombu_arg_to_any(models, kwargs[arg_k])

    except KeyError:
        # this is a celery -> celery message
        pass

    return data
