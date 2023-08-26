# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import sqlalchemy_2_0

from celery_sqlalchemy.schema import TypeMap

# system imports
from typing import Any
from typing import List

# dependency imports
from pytest import mark

from sqlalchemy.sql import sqltypes


@mark.parametrize(
    "type",
    [
        [sqltypes.Double, "double_from_json", "double_params", "double_to_json"],
        [sqltypes.UUID, "uuid_from_json", "uuid_params", "uuid_to_json"],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert sqlalchemy_2_0.type_maps[type[0]] == TypeMap(
        from_json=type[1], params=type[2], to_json=type[3]
    )
