# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.schema import Field
from celery_sqlalchemy.schema import Schema

# system dependencies
from unittest.mock import Mock


def test_field() -> None:
    Field(name=Mock(), type=Mock(), value_in=Mock(), value_out=Mock())


def test_schema() -> None:
    Schema(fields=Mock(), model=Mock())
