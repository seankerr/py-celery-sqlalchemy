# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from .model_postgresql import postgresql_type_maps

from .schema import Field
from .schema import Schema
from .schema import TypeMap

# system imports
from importlib import import_module

from types import ModuleType

from typing import Dict
from typing import cast

# dependency imports
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
                from_json=getattr(
                    interface, type_maps[column.type.__class__].from_json
                ),
                name=column.name,
                params=get_params(column),
                to_json=getattr(interface, type_maps[column.type.__class__].to_json),
                type=column.type.__class__,
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


type_maps = {
    # ----------------------------------------------------------------------------------
    # Base SQLAlchemy types
    # ----------------------------------------------------------------------------------
    sqltypes.ARRAY: TypeMap(
        from_json="array_from_json", params="array_params", to_json="array_to_json"
    ),
    sqltypes.BigInteger: TypeMap(
        from_json="big_integer_from_json",
        params="big_integer_params",
        to_json="big_integer_to_json",
    ),
    sqltypes.Boolean: TypeMap(
        from_json="boolean_from_json",
        params="boolean_params",
        to_json="boolean_to_json",
    ),
    sqltypes.Date: TypeMap(
        from_json="date_from_json", params="date_params", to_json="date_to_json"
    ),
    sqltypes.DateTime: TypeMap(
        from_json="date_time_from_json",
        params="date_time_params",
        to_json="date_time_to_json",
    ),
    sqltypes.Double: TypeMap(
        from_json="double_from_json", params="double_params", to_json="double_to_json"
    ),
    sqltypes.Enum: TypeMap(
        from_json="enum_from_json", params="enum_params", to_json="enum_to_json"
    ),
    sqltypes.Float: TypeMap(
        from_json="float_from_json", params="float_params", to_json="float_to_json"
    ),
    sqltypes.Integer: TypeMap(
        from_json="integer_from_json",
        params="integer_params",
        to_json="integer_to_json",
    ),
    sqltypes.Interval: TypeMap(
        from_json="interval_from_json",
        params="interval_params",
        to_json="interval_to_json",
    ),
    sqltypes.LargeBinary: TypeMap(
        from_json="large_binary_from_json",
        params="large_binary_params",
        to_json="large_binary_to_json",
    ),
    sqltypes.JSON: TypeMap(
        from_json="json_from_json", params="json_params", to_json="json_to_json"
    ),
    sqltypes.Numeric: TypeMap(
        from_json="numeric_from_json",
        params="numeric_params",
        to_json="numeric_to_json",
    ),
    sqltypes.SmallInteger: TypeMap(
        from_json="small_integer_from_json",
        params="small_integer_params",
        to_json="small_integer_to_json",
    ),
    sqltypes.String: TypeMap(
        from_json="string_from_json", params="string_params", to_json="string_to_json"
    ),
    sqltypes.Text: TypeMap(
        from_json="text_from_json", params="text_params", to_json="text_to_json"
    ),
    sqltypes.Time: TypeMap(
        from_json="time_from_json", params="time_params", to_json="time_to_json"
    ),
    sqltypes.Unicode: TypeMap(
        from_json="unicode_from_json",
        params="unicode_params",
        to_json="unicode_to_json",
    ),
    sqltypes.UnicodeText: TypeMap(
        from_json="unicode_text_from_json",
        params="unicode_text_params",
        to_json="unicode_text_to_json",
    ),
    sqltypes.UUID: TypeMap(
        from_json="uuid_from_json", params="uuid_params", to_json="uuid_to_json"
    ),
    # ----------------------------------------------------------------------------------
    # Dialect specific types
    # ----------------------------------------------------------------------------------
    **postgresql_type_maps,
}
