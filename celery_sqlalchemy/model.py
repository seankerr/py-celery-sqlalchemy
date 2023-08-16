# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# system imports
from abc import ABC

from dataclasses import dataclass

from types import ModuleType

from typing import Any
from typing import Callable
from typing import List
from typing import cast

# dependency imports
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapper

from sqlalchemy import inspect


def initialize(models: List[Any]) -> None:
    """
    Initialize the list of serializable models.

    Parameters:
        models (list): A combination of model classes or modules containing model
            classes to be discovered.

    Raises:
        InvalidRequestError: Model class is invalid.
    """
    if not len(models):
        raise ValueError("No models were specified")

    if isinstance(models[0], ModuleType):
        for module in models:
            _discover(module)

    else:
        for model in models:
            try:
                mapper = cast(Mapper, inspect(model))

            except NoInspectionAvailable:
                raise InvalidRequestError(
                    f"Model class {model.__class__} is not a valid SQLAlchemy model"
                )

            _map_model(model, mapper)


def _discover(module: Any) -> None:
    """
    Discover model classes within an object or module.

    Parameters:
        module (object): The object or module to search.
    """
    for entry in dir(module):
        try:
            mapper = cast(Mapper, inspect(entry))

        except NoInspectionAvailable:
            continue

        _map_model(cast(DeclarativeBase, entry), mapper)


def _map_model(model: DeclarativeBase, mapper: Mapper) -> None:
    """
    Map a model into its serialization and deserialization structure.

    Parameters:
        mapper (Mapper): Model mapper.
    """
    for entry in dir(mapper):
        if "model" in entry:
            print(entry)

    for column in mapper.columns:
        print(column.type.__class__)


# --------------------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Field:
    name: str
    type: type
    value_in: Callable
    value_out: Callable


class Schema(ABC):
    fields: List[Field]

    def from_message(self, message: Any) -> Any:
        """
        Returns a deserialized model.

        Parameters:
            message (object): Message.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.to_message() is not implemented"
        )

    def to_message(self, model: Any) -> Any:
        """
        Returns a serialized model.

        Parameters:
            model (object): Model.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}.to_message() is not implemented"
        )
