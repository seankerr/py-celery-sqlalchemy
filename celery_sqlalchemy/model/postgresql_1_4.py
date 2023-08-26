# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import TypeMap

# dependency imports
from sqlalchemy.dialects.postgresql import ARRAY as POSTGRESQL_ARRAY
from sqlalchemy.dialects.postgresql import BIT as POSTGRESQL_BIT
from sqlalchemy.dialects.postgresql import BYTEA as POSTGRESQL_BYTEA
from sqlalchemy.dialects.postgresql import CIDR as POSTGRESQL_CIDR
from sqlalchemy.dialects.postgresql import DATERANGE as POSTGRESQL_DATERANGE
from sqlalchemy.dialects.postgresql import (
    DOUBLE_PRECISION as POSTGRESQL_DOUBLE_PRECISION,
)
from sqlalchemy.dialects.postgresql import ENUM as POSTGRESQL_ENUM
from sqlalchemy.dialects.postgresql import HSTORE as POSTGRESQL_HSTORE
from sqlalchemy.dialects.postgresql import INT4RANGE as POSTGRESQL_INT4RANGE
from sqlalchemy.dialects.postgresql import INT8RANGE as POSTGRESQL_INT8RANGE
from sqlalchemy.dialects.postgresql import INET as POSTGRESQL_INET
from sqlalchemy.dialects.postgresql import INTERVAL as POSTGRESQL_INTERVAL
from sqlalchemy.dialects.postgresql import JSON as POSTGRESQL_JSON
from sqlalchemy.dialects.postgresql import JSONB as POSTGRESQL_JSONB
from sqlalchemy.dialects.postgresql import MACADDR as POSTGRESQL_MACADDR
from sqlalchemy.dialects.postgresql import MONEY as POSTGRESQL_MONEY
from sqlalchemy.dialects.postgresql import NUMRANGE as POSTGRESQL_NUMRANGE
from sqlalchemy.dialects.postgresql import OID as POSTGRESQL_OID
from sqlalchemy.dialects.postgresql import REAL as POSTGRESQL_REAL
from sqlalchemy.dialects.postgresql import REGCLASS as POSTGRESQL_REGCLASS
from sqlalchemy.dialects.postgresql import TIME as POSTGRESQL_TIME
from sqlalchemy.dialects.postgresql import TIMESTAMP as POSTGRESQL_TIMESTAMP
from sqlalchemy.dialects.postgresql import TSRANGE as POSTGRESQL_TSRANGE
from sqlalchemy.dialects.postgresql import TSTZRANGE as POSTGRESQL_TSTZRANGE
from sqlalchemy.dialects.postgresql import TSVECTOR as POSTGRESQL_TSVECTOR

type_maps = {
    POSTGRESQL_ARRAY: TypeMap(
        from_json="postgresql_array_from_json",
        params="postgresql_array_params",
        to_json="postgresql_array_to_json",
    ),
    POSTGRESQL_BIT: TypeMap(
        from_json="postgresql_bit_from_json",
        params="postgresql_bit_params",
        to_json="postgresql_bit_to_json",
    ),
    POSTGRESQL_BYTEA: TypeMap(
        from_json="postgresql_bytea_from_json",
        params="postgresql_bytea_params",
        to_json="postgresql_bytea_to_json",
    ),
    POSTGRESQL_CIDR: TypeMap(
        from_json="postgresql_cidr_from_json",
        params="postgresql_cidr_params",
        to_json="postgresql_cidr_to_json",
    ),
    POSTGRESQL_DATERANGE: TypeMap(
        from_json="postgresql_daterange_from_json",
        params="postgresql_daterange_params",
        to_json="postgresql_daterange_to_json",
    ),
    POSTGRESQL_DOUBLE_PRECISION: TypeMap(
        from_json="postgresql_double_precision_from_json",
        params="postgresql_double_precision_params",
        to_json="postgresql_double_precision_to_json",
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
    POSTGRESQL_INT8RANGE: TypeMap(
        from_json="postgresql_int8range_from_json",
        params="postgresql_int8range_params",
        to_json="postgresql_int8range_to_json",
    ),
    POSTGRESQL_INET: TypeMap(
        from_json="postgresql_inet_from_json",
        params="postgresql_inet_params",
        to_json="postgresql_inet_to_json",
    ),
    POSTGRESQL_INTERVAL: TypeMap(
        from_json="postgresql_interval_from_json",
        params="postgresql_interval_params",
        to_json="postgresql_interval_to_json",
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
    POSTGRESQL_MACADDR: TypeMap(
        from_json="postgresql_macaddr_from_json",
        params="postgresql_macaddr_params",
        to_json="postgresql_macaddr_to_json",
    ),
    POSTGRESQL_MONEY: TypeMap(
        from_json="postgresql_money_from_json",
        params="postgresql_money_params",
        to_json="postgresql_money_to_json",
    ),
    POSTGRESQL_NUMRANGE: TypeMap(
        from_json="postgresql_numrange_from_json",
        params="postgresql_numrange_params",
        to_json="postgresql_numrange_to_json",
    ),
    POSTGRESQL_OID: TypeMap(
        from_json="postgresql_oid_from_json",
        params="postgresql_oid_params",
        to_json="postgresql_oid_to_json",
    ),
    POSTGRESQL_REAL: TypeMap(
        from_json="postgresql_real_from_json",
        params="postgresql_real_params",
        to_json="postgresql_real_to_json",
    ),
    POSTGRESQL_REGCLASS: TypeMap(
        from_json="postgresql_regclass_from_json",
        params="postgresql_regclass_params",
        to_json="postgresql_regclass_to_json",
    ),
    POSTGRESQL_TIME: TypeMap(
        from_json="postgresql_time_from_json",
        params="postgresql_time_params",
        to_json="postgresql_time_to_json",
    ),
    POSTGRESQL_TIMESTAMP: TypeMap(
        from_json="postgresql_timestamp_from_json",
        params="postgresql_timestamp_params",
        to_json="postgresql_timestamp_to_json",
    ),
    POSTGRESQL_TSRANGE: TypeMap(
        from_json="postgresql_tsrange_from_json",
        params="postgresql_tsrange_params",
        to_json="postgresql_tsrange_to_json",
    ),
    POSTGRESQL_TSTZRANGE: TypeMap(
        from_json="postgresql_tstzrange_from_json",
        params="postgresql_tstzrange_params",
        to_json="postgresql_tstzrange_to_json",
    ),
    POSTGRESQL_TSVECTOR: TypeMap(
        from_json="postgresql_tsvector_from_json",
        params="postgresql_tsvector_params",
        to_json="postgresql_tsvector_to_json",
    ),
}
