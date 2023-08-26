# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import TypeMap

try:
    # dependency imports
    from sqlalchemy.dialects.postgresql import CITEXT as POSTGRESQL_CITEXT
    from sqlalchemy.dialects.postgresql import (
        DATEMULTIRANGE as POSTGRESQL_DATEMULTIRANGE,
    )
    from sqlalchemy.dialects.postgresql import DOMAIN as POSTGRESQL_DOMAIN
    from sqlalchemy.dialects.postgresql import (
        INT4MULTIRANGE as POSTGRESQL_INT4MULTIRANGE,
    )
    from sqlalchemy.dialects.postgresql import (
        INT8MULTIRANGE as POSTGRESQL_INT8MULTIRANGE,
    )
    from sqlalchemy.dialects.postgresql import JSONPATH as POSTGRESQL_JSONPATH
    from sqlalchemy.dialects.postgresql import MACADDR8 as POSTGRESQL_MACADDR8
    from sqlalchemy.dialects.postgresql import NUMMULTIRANGE as POSTGRESQL_NUMMULTIRANGE
    from sqlalchemy.dialects.postgresql import REGCONFIG as POSTGRESQL_REGCONFIG
    from sqlalchemy.dialects.postgresql import TSQUERY as POSTGRESQL_TSQUERY
    from sqlalchemy.dialects.postgresql import TSMULTIRANGE as POSTGRESQL_TSMULTIRANGE
    from sqlalchemy.dialects.postgresql import (
        TSTZMULTIRANGE as POSTGRESQL_TSTZMULTIRANGE,
    )
    from sqlalchemy.dialects.postgresql import TSVECTOR as POSTGRESQL_TSVECTOR

    type_maps = {
        POSTGRESQL_CITEXT: TypeMap(
            from_json="postgresql_citext_from_json",
            params="postgresql_citext_params",
            to_json="postgresql_citext_to_json",
        ),
        POSTGRESQL_DATEMULTIRANGE: TypeMap(
            from_json="postgresql_datemultirange_from_json",
            params="postgresql_datemultirange_params",
            to_json="postgresql_datemultirange_to_json",
        ),
        POSTGRESQL_DOMAIN: TypeMap(
            from_json="postgresql_domain_from_json",
            params="postgresql_domain_params",
            to_json="postgresql_domain_to_json",
        ),
        POSTGRESQL_INT4MULTIRANGE: TypeMap(
            from_json="postgresql_int4multirange_from_json",
            params="postgresql_int4multirange_params",
            to_json="postgresql_int4multirange_to_json",
        ),
        POSTGRESQL_INT8MULTIRANGE: TypeMap(
            from_json="postgresql_int8multirange_from_json",
            params="postgresql_int8multirange_params",
            to_json="postgresql_int8multirange_to_json",
        ),
        POSTGRESQL_JSONPATH: TypeMap(
            from_json="postgresql_jsonpath_from_json",
            params="postgresql_jsonpath_params",
            to_json="postgresql_jsonpath_to_json",
        ),
        POSTGRESQL_MACADDR8: TypeMap(
            from_json="postgresql_macaddr8_from_json",
            params="postgresql_macaddr8_params",
            to_json="postgresql_macaddr8_to_json",
        ),
        POSTGRESQL_NUMMULTIRANGE: TypeMap(
            from_json="postgresql_nummultirange_from_json",
            params="postgresql_nummultirange_params",
            to_json="postgresql_nummultirange_to_json",
        ),
        POSTGRESQL_REGCONFIG: TypeMap(
            from_json="postgresql_regconfig_from_json",
            params="postgresql_regconfig_params",
            to_json="postgresql_regconfig_to_json",
        ),
        POSTGRESQL_TSQUERY: TypeMap(
            from_json="postgresql_tsquery_from_json",
            params="postgresql_tsquery_params",
            to_json="postgresql_tsquery_to_json",
        ),
        POSTGRESQL_TSMULTIRANGE: TypeMap(
            from_json="postgresql_tsmultirange_from_json",
            params="postgresql_tsmultirange_params",
            to_json="postgresql_tsmultirange_to_json",
        ),
        POSTGRESQL_TSTZMULTIRANGE: TypeMap(
            from_json="postgresql_tstzmultirange_from_json",
            params="postgresql_tstzmultirange_params",
            to_json="postgresql_tstzmultirange_to_json",
        ),
        POSTGRESQL_TSVECTOR: TypeMap(
            from_json="postgresql_tsvector_from_json",
            params="postgresql_tsvector_params",
            to_json="postgresql_tsvector_to_json",
        ),
    }

except Exception:
    type_maps = {}
