# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

"""
SQLAlchemy model serialization for celery.
"""

# celery-sqlalchemy imports
from . import errors

# system imports
from importlib import import_module

from typing import Any

# dependency imports
from celery import Celery


def initialize(
    celery: Celery,
    interface: str = "json",
    **interface_args: Any,
) -> None:
    """
    Initialize the serializer with models.

    Parameters:
        celery (Celery): Celery instance.
        interface (str): Serialization interface.
        interface_args (dict): Initialization arguments to pass to the interface.
    """
    try:
        interface_module = import_module(f".{interface}", package="celery_sqlalchemy")

    except ModuleNotFoundError:
        raise errors.UnsupportedInterfaceError(
            f"Unsupported serialization interface '{interface}'"
        )

    interface_module.initialize(celery, **interface_args)
