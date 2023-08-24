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
from sqlalchemy.dialects.postgresql import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql import INT4RANGE as POSTGRESQL_INT4RANGE
from sqlalchemy.dialects.postgresql import INT4MULTIRANGE as POSTGRESQL_INT4MULTIRANGE
from sqlalchemy.dialects.postgresql import INT8RANGE as POSTGRESQL_INT8RANGE
from sqlalchemy.dialects.postgresql import INT8MULTIRANGE as POSTGRESQL_INT8MULTIRANGE
from sqlalchemy.dialects.postgresql import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql import JSONB as POSTGRESQL_JSONB
from sqlalchemy.dialects.postgresql import JSONPATH as POSTGRESQL_JSONPATH
from sqlalchemy.dialects.postgresql import NUMRANGE as POSTGRESQL_NUMRANGE
from sqlalchemy.dialects.postgresql import NUMMULTIRANGE as POSTGRESQL_NUMMULTIRANGE
from sqlalchemy.dialects.postgresql import TSRANGE as POSTGRESQL_TSRANGE
from sqlalchemy.dialects.postgresql import TSMULTIRANGE as POSTGRESQL_TSMULTIRANGE
from sqlalchemy.dialects.postgresql import TSTZRANGE as POSTGRESQL_TSTZRANGE
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE as POSTGRESQL_TSTZMULTIRANGE

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


@dataclass(frozen=True)
class TypeMap:
    from_json: str
    params: Any
    to_json: str


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
    POSTGRESQL_ARRAY: TypeMap(
        from_json="postgresql_array_from_json",
        params="postgresql_array_params",
        to_json="postgresql_array_to_json",
    ),
    POSTGRESQL_ENUM: TypeMap(
        from_json="postgresql_enum_from_json",
        params="postgresql_enum_params",
        to_json="postgresql_enum_to_json",
    ),
    POSTGRESQL_HSTORE: TypeMap(
        from_json="postgresql_hstore_from_json",
        params="postgresql_hstore_params",
        to_json="postgresql_hstore_to_json",
    ),
    POSTGRESQL_INT4RANGE: TypeMap(
        from_json="postgresql_int4range_from_json",
        params="postgresql_int4range_params",
        to_json="postgresql_int4range_to_json",
    ),
    POSTGRESQL_INT4MULTIRANGE: TypeMap(
        from_json="postgresql_int4multirange_from_json",
        params="postgresql_int4multirange_params",
        to_json="postgresql_int4multirange_to_json",
    ),
    POSTGRESQL_INT8RANGE: TypeMap(
        from_json="postgresql_int8range_from_json",
        params="postgresql_int8range_params",
        to_json="postgresql_int8range_to_json",
    ),
    POSTGRESQL_INT8MULTIRANGE: TypeMap(
        from_json="postgresql_int8multirange_from_json",
        params="postgresql_int8multirange_params",
        to_json="postgresql_int8multirange_to_json",
    ),
    POSTGRESQL_JSON: TypeMap(
        from_json="postgresql_json_from_json",
        params="postgresql_json_params",
        to_json="postgresql_json_to_json",
    ),
    POSTGRESQL_JSONB: TypeMap(
        from_json="postgresql_jsonb_from_json",
        params="postgresql_jsonb_params",
        to_json="postgresql_jsonb_to_json",
    ),
    POSTGRESQL_JSONPATH: TypeMap(
        from_json="postgresql_jsonpath_from_json",
        params="postgresql_jsonpath_params",
        to_json="postgresql_jsonpath_to_json",
    ),
    POSTGRESQL_NUMRANGE: TypeMap(
        from_json="postgresql_numrange_from_json",
        params="postgresql_numrange_params",
        to_json="postgresql_numrange_to_json",
    ),
    POSTGRESQL_NUMMULTIRANGE: TypeMap(
        from_json="postgresql_nummultirange_from_json",
        params="postgresql_nummultirange_params",
        to_json="postgresql_nummultirange_to_json",
    ),
    POSTGRESQL_TSRANGE: TypeMap(
        from_json="postgresql_tsrange_from_json",
        params="postgresql_tsrange_params",
        to_json="postgresql_tsrange_to_json",
    ),
    POSTGRESQL_TSMULTIRANGE: TypeMap(
        from_json="postgresql_tsmultirange_from_json",
        params="postgresql_tsmultirange_params",
        to_json="postgresql_tsmultirange_to_json",
    ),
    POSTGRESQL_TSTZRANGE: TypeMap(
        from_json="postgresql_tstzrange_from_json",
        params="postgresql_tstzrange_params",
        to_json="postgresql_tstzrange_to_json",
    ),
    POSTGRESQL_TSTZMULTIRANGE: TypeMap(
        from_json="postgresql_tstzmultirange_from_json",
        params="postgresql_tstzmultirange_params",
        to_json="postgresql_tstzmultirange_to_json",
    ),
}
