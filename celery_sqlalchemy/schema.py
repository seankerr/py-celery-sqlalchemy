# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# system imports
from abc import ABC

from dataclasses import dataclass

from typing import Any
from typing import Callable
from typing import List


@dataclass(frozen=True)
class Field:
    name: str
    type: type
    value_in: Callable
    value_out: Callable


@dataclass(frozen=True)
class Schema(ABC):
    fields: List[Field]
    model: Any
