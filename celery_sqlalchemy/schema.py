# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# system imports
from abc import ABC

from dataclasses import dataclass

from typing import Any
from typing import Callable
from typing import Generic
from typing import List
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Field(Generic[T]):
    from_json: Callable
    name: str
    params: T
    to_json: Callable
    type: type


@dataclass(frozen=True)
class Schema(ABC):
    fields: List[Field]
    model: Any


@dataclass(frozen=True)
class TypeMap:
    from_json: str
    params: Any
    to_json: str
