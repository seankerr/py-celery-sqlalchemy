# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

"""
SQLAlchemy model serialization for celery.
"""

# celery-sqlalchemy imports
from . import kombu
from . import model

# system imports
from typing import Any
from typing import List

# dependency imports
from celery import Celery


def initialize(celery: Celery, models: List[Any]) -> None:
    """
    Initialize the serializer with models.

    Parameters:
        celery (Celery): Celery instance.
        models (list): A combination of model classes or modules containing model
            classes to be discovered.
    """
    kombu.initialize(celery)
    model.initialize(models)
