# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import postgresql_1_4

from celery_sqlalchemy.schema import TypeMap

# system imports
from typing import Any
from typing import List

# dependency imports
from pytest import mark

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


@mark.parametrize(
    "type",
    [
        [
            POSTGRESQL_ARRAY,
            "postgresql_array_from_json",
            "postgresql_array_params",
            "postgresql_array_to_json",
        ],
        [
            POSTGRESQL_BIT,
            "postgresql_bit_from_json",
            "postgresql_bit_params",
            "postgresql_bit_to_json",
        ],
        [
            POSTGRESQL_BYTEA,
            "postgresql_bytea_from_json",
            "postgresql_bytea_params",
            "postgresql_bytea_to_json",
        ],
        [
            POSTGRESQL_CIDR,
            "postgresql_cidr_from_json",
            "postgresql_cidr_params",
            "postgresql_cidr_to_json",
        ],
        [
            POSTGRESQL_DATERANGE,
            "postgresql_daterange_from_json",
            "postgresql_daterange_params",
            "postgresql_daterange_to_json",
        ],
        [
            POSTGRESQL_DOUBLE_PRECISION,
            "postgresql_double_precision_from_json",
            "postgresql_double_precision_params",
            "postgresql_double_precision_to_json",
        ],
        [
            POSTGRESQL_ENUM,
            "postgresql_enum_from_json",
            "postgresql_enum_params",
            "postgresql_enum_to_json",
        ],
        [
            POSTGRESQL_HSTORE,
            "postgresql_hstore_from_json",
            "postgresql_hstore_params",
            "postgresql_hstore_to_json",
        ],
        [
            POSTGRESQL_INT4RANGE,
            "postgresql_int4range_from_json",
            "postgresql_int4range_params",
            "postgresql_int4range_to_json",
        ],
        [
            POSTGRESQL_INT8RANGE,
            "postgresql_int8range_from_json",
            "postgresql_int8range_params",
            "postgresql_int8range_to_json",
        ],
        [
            POSTGRESQL_INET,
            "postgresql_inet_from_json",
            "postgresql_inet_params",
            "postgresql_inet_to_json",
        ],
        [
            POSTGRESQL_INTERVAL,
            "postgresql_interval_from_json",
            "postgresql_interval_params",
            "postgresql_interval_to_json",
        ],
        [
            POSTGRESQL_JSON,
            "postgresql_json_from_json",
            "postgresql_json_params",
            "postgresql_json_to_json",
        ],
        [
            POSTGRESQL_JSONB,
            "postgresql_jsonb_from_json",
            "postgresql_jsonb_params",
            "postgresql_jsonb_to_json",
        ],
        [
            POSTGRESQL_MACADDR,
            "postgresql_macaddr_from_json",
            "postgresql_macaddr_params",
            "postgresql_macaddr_to_json",
        ],
        [
            POSTGRESQL_MONEY,
            "postgresql_money_from_json",
            "postgresql_money_params",
            "postgresql_money_to_json",
        ],
        [
            POSTGRESQL_NUMRANGE,
            "postgresql_numrange_from_json",
            "postgresql_numrange_params",
            "postgresql_numrange_to_json",
        ],
        [
            POSTGRESQL_OID,
            "postgresql_oid_from_json",
            "postgresql_oid_params",
            "postgresql_oid_to_json",
        ],
        [
            POSTGRESQL_REAL,
            "postgresql_real_from_json",
            "postgresql_real_params",
            "postgresql_real_to_json",
        ],
        [
            POSTGRESQL_REGCLASS,
            "postgresql_regclass_from_json",
            "postgresql_regclass_params",
            "postgresql_regclass_to_json",
        ],
        [
            POSTGRESQL_TIME,
            "postgresql_time_from_json",
            "postgresql_time_params",
            "postgresql_time_to_json",
        ],
        [
            POSTGRESQL_TIMESTAMP,
            "postgresql_timestamp_from_json",
            "postgresql_timestamp_params",
            "postgresql_timestamp_to_json",
        ],
        [
            POSTGRESQL_TSRANGE,
            "postgresql_tsrange_from_json",
            "postgresql_tsrange_params",
            "postgresql_tsrange_to_json",
        ],
        [
            POSTGRESQL_TSTZRANGE,
            "postgresql_tstzrange_from_json",
            "postgresql_tstzrange_params",
            "postgresql_tstzrange_to_json",
        ],
        [
            POSTGRESQL_TSVECTOR,
            "postgresql_tsvector_from_json",
            "postgresql_tsvector_params",
            "postgresql_tsvector_to_json",
        ],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert postgresql_1_4.type_maps[type[0]] == TypeMap(
        from_json=type[1], params=type[2], to_json=type[3]
    )
