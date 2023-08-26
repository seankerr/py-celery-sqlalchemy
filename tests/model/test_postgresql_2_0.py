# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy.model import postgresql_2_0

from celery_sqlalchemy.schema import TypeMap

# system imports
from typing import Any
from typing import List

# dependency imports
from pytest import mark

from sqlalchemy.dialects.postgresql import CITEXT as POSTGRESQL_CITEXT
from sqlalchemy.dialects.postgresql import DATEMULTIRANGE as POSTGRESQL_DATEMULTIRANGE
from sqlalchemy.dialects.postgresql import DOMAIN as POSTGRESQL_DOMAIN
from sqlalchemy.dialects.postgresql import INT4MULTIRANGE as POSTGRESQL_INT4MULTIRANGE
from sqlalchemy.dialects.postgresql import INT8MULTIRANGE as POSTGRESQL_INT8MULTIRANGE
from sqlalchemy.dialects.postgresql import JSONPATH as POSTGRESQL_JSONPATH
from sqlalchemy.dialects.postgresql import MACADDR8 as POSTGRESQL_MACADDR8
from sqlalchemy.dialects.postgresql import NUMMULTIRANGE as POSTGRESQL_NUMMULTIRANGE
from sqlalchemy.dialects.postgresql import REGCONFIG as POSTGRESQL_REGCONFIG
from sqlalchemy.dialects.postgresql import TSQUERY as POSTGRESQL_TSQUERY
from sqlalchemy.dialects.postgresql import TSMULTIRANGE as POSTGRESQL_TSMULTIRANGE
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE as POSTGRESQL_TSTZMULTIRANGE


@mark.parametrize(
    "type",
    [
        [
            POSTGRESQL_CITEXT,
            "postgresql_citext_from_json",
            "postgresql_citext_params",
            "postgresql_citext_to_json",
        ],
        [
            POSTGRESQL_DATEMULTIRANGE,
            "postgresql_datemultirange_from_json",
            "postgresql_datemultirange_params",
            "postgresql_datemultirange_to_json",
        ],
        [
            POSTGRESQL_DOMAIN,
            "postgresql_domain_from_json",
            "postgresql_domain_params",
            "postgresql_domain_to_json",
        ],
        [
            POSTGRESQL_INT4MULTIRANGE,
            "postgresql_int4multirange_from_json",
            "postgresql_int4multirange_params",
            "postgresql_int4multirange_to_json",
        ],
        [
            POSTGRESQL_INT8MULTIRANGE,
            "postgresql_int8multirange_from_json",
            "postgresql_int8multirange_params",
            "postgresql_int8multirange_to_json",
        ],
        [
            POSTGRESQL_JSONPATH,
            "postgresql_jsonpath_from_json",
            "postgresql_jsonpath_params",
            "postgresql_jsonpath_to_json",
        ],
        [
            POSTGRESQL_MACADDR8,
            "postgresql_macaddr8_from_json",
            "postgresql_macaddr8_params",
            "postgresql_macaddr8_to_json",
        ],
        [
            POSTGRESQL_NUMMULTIRANGE,
            "postgresql_nummultirange_from_json",
            "postgresql_nummultirange_params",
            "postgresql_nummultirange_to_json",
        ],
        [
            POSTGRESQL_REGCONFIG,
            "postgresql_regconfig_from_json",
            "postgresql_regconfig_params",
            "postgresql_regconfig_to_json",
        ],
        [
            POSTGRESQL_TSQUERY,
            "postgresql_tsquery_from_json",
            "postgresql_tsquery_params",
            "postgresql_tsquery_to_json",
        ],
        [
            POSTGRESQL_TSMULTIRANGE,
            "postgresql_tsmultirange_from_json",
            "postgresql_tsmultirange_params",
            "postgresql_tsmultirange_to_json",
        ],
        [
            POSTGRESQL_TSTZMULTIRANGE,
            "postgresql_tstzmultirange_from_json",
            "postgresql_tstzmultirange_params",
            "postgresql_tstzmultirange_to_json",
        ],
    ],
)
def test_type_maps(type: List[Any]) -> None:
    assert postgresql_2_0.type_maps[type[0]] == TypeMap(
        from_json=type[1], params=type[2], to_json=type[3]
    )
