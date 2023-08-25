# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import Field

# system imports
from typing import Any
from typing import List
from typing import Optional

# dependency imports
from sqlalchemy import Column


def postgresql_array_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_array_params(column: Column) -> Any:
    return


def postgresql_array_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_bit_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_bit_params(column: Column) -> Any:
    return


def postgresql_bit_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_bytea_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_bytea_params(column: Column) -> Any:
    return


def postgresql_bytea_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_cidr_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_cidr_params(column: Column) -> Any:
    return


def postgresql_cidr_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_citext_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_citext_params(column: Column) -> Any:
    return


def postgresql_citext_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_daterange_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_daterange_params(column: Column) -> Any:
    return


def postgresql_daterange_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_datemultirange_from_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_datemultirange_params(column: Column) -> Any:
    return


def postgresql_datemultirange_to_json(
    field: Field, value: Optional[List[Any]]
) -> Optional[List[Any]]:
    return value


def postgresql_domain_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_domain_params(column: Column) -> Any:
    return


def postgresql_domain_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_double_precision_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_double_precision_params(column: Column) -> Any:
    return


def postgresql_double_precision_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_enum_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_enum_params(column: Column) -> Any:
    return


def postgresql_enum_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_hstore_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_hstore_params(column: Column) -> Any:
    return


def postgresql_hstore_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4range_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4range_params(column: Column) -> Any:
    return


def postgresql_int4range_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int4multirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int4multirange_params(column: Column) -> Any:
    return


def postgresql_int4multirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int8range_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int8range_params(column: Column) -> Any:
    return


def postgresql_int8range_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_int8multirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_int8multirange_params(column: Column) -> Any:
    return


def postgresql_int8multirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_inet_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_inet_params(column: Column) -> Any:
    return


def postgresql_inet_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_interval_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_interval_params(column: Column) -> Any:
    return


def postgresql_interval_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_json_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_json_params(column: Column) -> Any:
    return


def postgresql_json_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonb_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonb_params(column: Column) -> Any:
    return


def postgresql_jsonb_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonpath_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_jsonpath_params(column: Column) -> Any:
    return


def postgresql_jsonpath_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_macaddr_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_macaddr_params(column: Column) -> Any:
    return


def postgresql_macaddr_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_macaddr8_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_macaddr8_params(column: Column) -> Any:
    return


def postgresql_macaddr8_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_money_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_money_params(column: Column) -> Any:
    return


def postgresql_money_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_numrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_numrange_params(column: Column) -> Any:
    return


def postgresql_numrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_nummultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_nummultirange_params(column: Column) -> Any:
    return


def postgresql_nummultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_oid_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_oid_params(column: Column) -> Any:
    return


def postgresql_oid_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_real_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_real_params(column: Column) -> Any:
    return


def postgresql_real_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_regclass_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_regclass_params(column: Column) -> Any:
    return


def postgresql_regclass_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_regconfig_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_regconfig_params(column: Column) -> Any:
    return


def postgresql_regconfig_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_time_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_time_params(column: Column) -> Any:
    return


def postgresql_time_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_timestamp_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_timestamp_params(column: Column) -> Any:
    return


def postgresql_timestamp_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsquery_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsquery_params(column: Column) -> Any:
    return


def postgresql_tsquery_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsrange_params(column: Column) -> Any:
    return


def postgresql_tsrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsmultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tsmultirange_params(column: Column) -> Any:
    return


def postgresql_tsmultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tstzrange_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tstzrange_params(column: Column) -> Any:
    return


def postgresql_tstzrange_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tstzmultirange_from_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tstzmultirange_params(column: Column) -> Any:
    return


def postgresql_tstzmultirange_to_json(
    field: Field, value: Optional[Any]
) -> Optional[Any]:
    return value


def postgresql_tsvector_from_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value


def postgresql_tsvector_params(column: Column) -> Any:
    return


def postgresql_tsvector_to_json(field: Field, value: Optional[Any]) -> Optional[Any]:
    return value
