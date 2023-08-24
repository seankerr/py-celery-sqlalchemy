# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.schema import Field
from celery_sqlalchemy.schema import Schema
from celery_sqlalchemy.schema import TypeMap

# system dependencies
from unittest.mock import Mock


def test_field() -> None:
    Field(from_json=Mock(), name=Mock(), params=Mock(), to_json=Mock(), type=Mock())


def test_schema() -> None:
    Schema(fields=Mock(), model=Mock())


def test_type_map() -> None:
    TypeMap(from_json=Mock(), params=Mock(), to_json=Mock())
