# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .schema import Field
from .schema import Schema

# system imports
from dataclasses import dataclass

from importlib import import_module

from types import ModuleType

from typing import Any
from typing import Dict
from typing import cast

# dependency imports
from sqlalchemy.dialects.postgresql.array import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql.named_types import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql.hstore import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql.json import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql.json import JSONB as POSTGRESQL_JSONB

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapper
from sqlalchemy.sql import sqltypes

from sqlalchemy import inspect

schema_maps: Dict[str, Schema] = {}


def add_schema(model: DeclarativeBase, mapper: Mapper, interface: ModuleType) -> Schema:
    """
    Returns a newly added schema.

    Parameters:
        model (DeclarativeBase): Model class.
        mapper (Mapper): Model mapper.
        interface (ModuleType): Serialization interface module.
    """
    schema = map_model(model, mapper, interface)

    schema_maps[schema_map_key(model)] = schema

    return schema


def load_model(model_path: str) -> DeclarativeBase:
    """
    Load a model from full its path name.

    Parameters:
        model_path (str): Full module and class name path.
    """
    package, model = model_path.rsplit(".", 1)
    module = import_module(package)

    return cast(DeclarativeBase, getattr(module, model))


def map_model(model: DeclarativeBase, mapper: Mapper, interface: ModuleType) -> Schema:
    """
    Map a model into its serialization and deserialization structure.

    Parameters:
        model (DeclarativeBase): Model class.
        mapper (Mapper): Model mapper.
        interface (ModuleType): Serialization interface module.
    """
    fields = []

    for column in mapper.columns:
        get_params = getattr(interface, type_maps[column.type.__class__].params)

        fields.append(
            Field(
                name=column.name,
                params=get_params(column.type),
                type=column.type.__class__,
                value_in=getattr(interface, type_maps[column.type.__class__].value_in),
                value_out=getattr(
                    interface, type_maps[column.type.__class__].value_out
                ),
            )
        )

    return Schema(fields=fields, model=model)


def schema_for_model(
    model: DeclarativeBase, mapper: Mapper, interface: ModuleType
) -> Schema:
    """
    Returns the schema for a model.

    Parameters:
        model (DeclarativeBase): Model class.
        mapper (Mapper): Model mapper.
        interface (ModuleType): Serialization interface module.
    """
    schema = schema_maps.get(schema_map_key(model))

    if not schema:
        schema = add_schema(model, mapper, interface)

    return schema


def schema_for_model_path(model_path: str, interface: ModuleType) -> Schema:
    """
    Returns the schema for a model path.

    Parameters:
        model_path (str): Full module and class name path.
        interface (ModuleType): Serialization interface module.
    """
    schema = schema_maps.get(model_path)

    if not schema:
        model = load_model(model_path)
        mapper = cast(Mapper, inspect(model))
        schema = add_schema(model, mapper, interface)

    return schema


def schema_map_key(model: DeclarativeBase) -> str:
    """
    Returns the schema map key for a model.

    Parameters:
        model (DeclarativeBase): Model class.
    """
    return f"{model.__module__}.{model.__class__.__name__}"


# --------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class TypeMap:
    params: Any
    value_in: str
    value_out: str


type_maps = {
    # ----------------------------------------------------------------------------------
    # Base SQLAlchemy types
    # ----------------------------------------------------------------------------------
    sqltypes.ARRAY: TypeMap(
        params="array_params", value_in="array_in", value_out="array_out"
    ),
    sqltypes.BigInteger: TypeMap(
        params="big_integer_params",
        value_in="big_integer_in",
        value_out="big_integer_out",
    ),
    sqltypes.Boolean: TypeMap(
        params="boolean_params", value_in="boolean_in", value_out="boolean_out"
    ),
    sqltypes.Date: TypeMap(
        params="date_params", value_in="date_in", value_out="date_out"
    ),
    sqltypes.DateTime: TypeMap(
        params="date_time_params", value_in="date_time_in", value_out="date_time_out"
    ),
    sqltypes.Double: TypeMap(
        params="double_params", value_in="double_in", value_out="double_out"
    ),
    sqltypes.Enum: TypeMap(
        params="enum_params", value_in="enum_in", value_out="enum_out"
    ),
    sqltypes.Float: TypeMap(
        params="float_params", value_in="float_in", value_out="float_out"
    ),
    sqltypes.Integer: TypeMap(
        params="integer_params", value_in="integer_in", value_out="integer_out"
    ),
    sqltypes.Interval: TypeMap(
        params="interval_params", value_in="interval_in", value_out="interval_out"
    ),
    sqltypes.LargeBinary: TypeMap(
        params="large_binary_params",
        value_in="large_binary_in",
        value_out="large_binary_out",
    ),
    sqltypes.JSON: TypeMap(
        params="json_params", value_in="json_in", value_out="json_out"
    ),
    sqltypes.Numeric: TypeMap(
        params="numeric_params", value_in="numeric_in", value_out="numeric_out"
    ),
    sqltypes.SmallInteger: TypeMap(
        params="small_integer_params",
        value_in="small_integer_in",
        value_out="small_integer_out",
    ),
    sqltypes.String: TypeMap(
        params="string_params", value_in="string_in", value_out="string_out"
    ),
    sqltypes.Text: TypeMap(
        params="text_params", value_in="text_in", value_out="text_out"
    ),
    sqltypes.Time: TypeMap(
        params="time_params", value_in="time_in", value_out="time_out"
    ),
    sqltypes.Unicode: TypeMap(
        params="unicode_params", value_in="unicode_in", value_out="unicode_out"
    ),
    sqltypes.UnicodeText: TypeMap(
        params="unicode_text_params",
        value_in="unicode_text_in",
        value_out="unicode_text_out",
    ),
    sqltypes.UUID: TypeMap(
        params="uuid_params", value_in="uuid_in", value_out="uuid_out"
    ),
    # ----------------------------------------------------------------------------------
    # Dialect specific types
    # ----------------------------------------------------------------------------------
    POSTGRESQL_ARRAY: TypeMap(
        params="postgresql_array_params",
        value_in="postgresql_array_in",
        value_out="postgresql_array_out",
    ),
    POSTGRESQL_ENUM: TypeMap(
        params="postgresql_enum_params",
        value_in="postgresql_enum_in",
        value_out="postgresql_enum_out",
    ),
    POSTGRESQL_HSTORE: TypeMap(
        params="postgresql_hstore_params",
        value_in="postgresql_hstore_in",
        value_out="postgresql_hstore_out",
    ),
    POSTGRESQL_JSON: TypeMap(
        params="postgresql_json_params",
        value_in="postgresql_json_in",
        value_out="postgresql_json_out",
    ),
    POSTGRESQL_JSONB: TypeMap(
        params="postgresql_jsonb_params",
        value_in="postgresql_jsonb_in",
        value_out="postgresql_jsonb_out",
    ),
}
