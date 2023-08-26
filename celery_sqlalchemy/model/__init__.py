# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from . import postgresql_1_4
from . import postgresql_2_0
from . import sqlalchemy_1_4
from . import sqlalchemy_2_0

from ..schema import Field
from ..schema import Schema

# system imports
from importlib import import_module

from types import ModuleType

from typing import Any
from typing import Dict
from typing import cast

# dependency imports
try:
    from sqlalchemy.orm import DeclarativeBase

except Exception:
    DeclarativeBase = Any

from sqlalchemy.orm import Mapper

from sqlalchemy import inspect

schema_maps: Dict[str, Schema] = {}
type_maps = {
    **sqlalchemy_1_4.type_maps,
    **sqlalchemy_2_0.type_maps,
    **postgresql_1_4.type_maps,
    **postgresql_2_0.type_maps,
}


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
