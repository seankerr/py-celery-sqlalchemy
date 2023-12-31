# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from celery_sqlalchemy.json import postgresql

# system imports
from unittest.mock import Mock
from unittest.mock import patch

PATH = "celery_sqlalchemy.json.postgresql"


def test_postgresql_array_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_array_from_json(field, value) == value


def test_postgresql_array_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_array_params(column)


def test_postgresql_array_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_array_to_json(field, value) == value


def test_postgresql_bit_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_bit_from_json(field, value) == value


def test_postgresql_bit_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_bit_params(column)


def test_postgresql_bit_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_bit_to_json(field, value) == value


def test_postgresql_bytea_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_bytea_from_json(field, value) == value


def test_postgresql_bytea_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_bytea_params(column)


def test_postgresql_bytea_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_bytea_to_json(field, value) == value


def test_postgresql_cidr_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_cidr_from_json(field, value) == value


def test_postgresql_cidr_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_cidr_params(column)


def test_postgresql_cidr_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_cidr_to_json(field, value) == value


def test_postgresql_citext_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_citext_from_json(field, value) == value


def test_postgresql_citext_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_citext_params(column)


def test_postgresql_citext_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_citext_to_json(field, value) == value


def test_postgresql_daterange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_daterange_from_json(field, value) == value


def test_postgresql_daterange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_daterange_params(column)


def test_postgresql_daterange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_daterange_to_json(field, value) == value


def test_postgresql_datemultirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_datemultirange_from_json(field, value) == value


def test_postgresql_datemultirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_datemultirange_params(column)


def test_postgresql_datemultirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_datemultirange_to_json(field, value) == value


def test_postgresql_domain_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_domain_from_json(field, value) == value


def test_postgresql_domain_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_domain_params(column)


def test_postgresql_domain_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_domain_to_json(field, value) == value


def test_postgresql_double_precision_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_double_precision_from_json(field, value) == value


def test_postgresql_double_precision_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_double_precision_params(column)


def test_postgresql_double_precision_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_double_precision_to_json(field, value) == value


def test_postgresql_enum_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_enum_from_json(field, value) == value


def test_postgresql_enum_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_enum_params(column)


def test_postgresql_enum_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_enum_to_json(field, value) == value


def test_postgresql_hstore_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_hstore_from_json(field, value) == value


def test_postgresql_hstore_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_hstore_params(column)


def test_postgresql_hstore_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_hstore_to_json(field, value) == value


def test_postgresql_int4range_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int4range_from_json(field, value) == value


def test_postgresql_int4range_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_int4range_params(column)


def test_postgresql_int4range_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int4range_to_json(field, value) == value


def test_postgresql_int4multirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int4multirange_from_json(field, value) == value


def test_postgresql_int4multirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_int4multirange_params(column)


def test_postgresql_int4multirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int4multirange_to_json(field, value) == value


def test_postgresql_int8range_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int8range_from_json(field, value) == value


def test_postgresql_int8range_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_int8range_params(column)


def test_postgresql_int8range_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int8range_to_json(field, value) == value


def test_postgresql_int8multirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int8multirange_from_json(field, value) == value


def test_postgresql_int8multirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_int8multirange_params(column)


def test_postgresql_int8multirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_int8multirange_to_json(field, value) == value


def test_postgresql_inet_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_inet_from_json(field, value) == value


def test_postgresql_inet_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_inet_params(column)


def test_postgresql_inet_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_inet_to_json(field, value) == value


def test_postgresql_interval_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_interval_from_json(field, value) == value


def test_postgresql_interval_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_interval_params(column)


def test_postgresql_interval_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_interval_to_json(field, value) == value


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_json_from_json(sqlalchemy: Mock) -> None:
    field = Mock()
    value = Mock()

    assert (
        postgresql.postgresql_json_from_json(field, value)
        == sqlalchemy.json_from_json.return_value
    )

    sqlalchemy.json_from_json.assert_called_with(field, value)


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_json_params(sqlalchemy: Mock) -> None:
    column = Mock()

    assert (
        postgresql.postgresql_json_params(column) == sqlalchemy.json_params.return_value
    )

    sqlalchemy.json_params.assert_called_with(column)


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_json_to_json(sqlalchemy: Mock) -> None:
    field = Mock()
    value = Mock()

    assert (
        postgresql.postgresql_json_to_json(field, value)
        == sqlalchemy.json_to_json.return_value
    )

    sqlalchemy.json_to_json.assert_called_with(field, value)


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_jsonb_from_json(sqlalchemy: Mock) -> None:
    field = Mock()
    value = Mock()

    assert (
        postgresql.postgresql_jsonb_from_json(field, value)
        == sqlalchemy.json_from_json.return_value
    )

    sqlalchemy.json_from_json.assert_called_with(field, value)


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_jsonb_params(sqlalchemy: Mock) -> None:
    column = Mock()

    assert (
        postgresql.postgresql_jsonb_params(column)
        == sqlalchemy.json_params.return_value
    )

    sqlalchemy.json_params.assert_called_with(column)


@patch(f"{PATH}.sqlalchemy")
def test_postgresql_jsonb_to_json(sqlalchemy: Mock) -> None:
    field = Mock()
    value = Mock()

    assert (
        postgresql.postgresql_jsonb_to_json(field, value)
        == sqlalchemy.json_to_json.return_value
    )

    sqlalchemy.json_to_json.assert_called_with(field, value)


def test_postgresql_jsonpath_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_jsonpath_from_json(field, value) == value


def test_postgresql_jsonpath_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_jsonpath_params(column)


def test_postgresql_jsonpath_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_jsonpath_to_json(field, value) == value


def test_postgresql_macaddr_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_macaddr_from_json(field, value) == value


def test_postgresql_macaddr_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_macaddr_params(column)


def test_postgresql_macaddr_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_macaddr_to_json(field, value) == value


def test_postgresql_macaddr8_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_macaddr8_from_json(field, value) == value


def test_postgresql_macaddr8_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_macaddr8_params(column)


def test_postgresql_macaddr8_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_macaddr8_to_json(field, value) == value


def test_postgresql_money_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_money_from_json(field, value) == value


def test_postgresql_money_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_money_params(column)


def test_postgresql_money_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_money_to_json(field, value) == value


def test_postgresql_numrange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_numrange_from_json(field, value) == value


def test_postgresql_numrange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_numrange_params(column)


def test_postgresql_numrange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_numrange_to_json(field, value) == value


def test_postgresql_nummultirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_nummultirange_from_json(field, value) == value


def test_postgresql_nummultirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_nummultirange_params(column)


def test_postgresql_nummultirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_nummultirange_to_json(field, value) == value


def test_postgresql_oid_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_oid_from_json(field, value) == value


def test_postgresql_oid_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_oid_params(column)


def test_postgresql_oid_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_oid_to_json(field, value) == value


def test_postgresql_real_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_real_from_json(field, value) == value


def test_postgresql_real_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_real_params(column)


def test_postgresql_real_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_real_to_json(field, value) == value


def test_postgresql_regclass_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_regclass_from_json(field, value) == value


def test_postgresql_regclass_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_regclass_params(column)


def test_postgresql_regclass_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_regclass_to_json(field, value) == value


def test_postgresql_regconfig_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_regconfig_from_json(field, value) == value


def test_postgresql_regconfig_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_regconfig_params(column)


def test_postgresql_regconfig_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_regconfig_to_json(field, value) == value


def test_postgresql_time_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_time_from_json(field, value) == value


def test_postgresql_time_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_time_params(column)


def test_postgresql_time_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_time_to_json(field, value) == value


def test_postgresql_timestamp_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_timestamp_from_json(field, value) == value


def test_postgresql_timestamp_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_timestamp_params(column)


def test_postgresql_timestamp_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_timestamp_to_json(field, value) == value


def test_postgresql_tsquery_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsquery_from_json(field, value) == value


def test_postgresql_tsquery_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tsquery_params(column)


def test_postgresql_tsquery_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsquery_to_json(field, value) == value


def test_postgresql_tsrange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsrange_from_json(field, value) == value


def test_postgresql_tsrange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tsrange_params(column)


def test_postgresql_tsrange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsrange_to_json(field, value) == value


def test_postgresql_tsmultirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsmultirange_from_json(field, value) == value


def test_postgresql_tsmultirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tsmultirange_params(column)


def test_postgresql_tsmultirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsmultirange_to_json(field, value) == value


def test_postgresql_tstzrange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tstzrange_from_json(field, value) == value


def test_postgresql_tstzrange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tstzrange_params(column)


def test_postgresql_tstzrange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tstzrange_to_json(field, value) == value


def test_postgresql_tstzmultirange_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tstzmultirange_from_json(field, value) == value


def test_postgresql_tstzmultirange_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tstzmultirange_params(column)


def test_postgresql_tstzmultirange_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tstzmultirange_to_json(field, value) == value


def test_postgresql_tsvector_from_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsvector_from_json(field, value) == value


def test_postgresql_tsvector_params() -> None:
    column = Mock()

    assert not postgresql.postgresql_tsvector_params(column)


def test_postgresql_tsvector_to_json() -> None:
    field = Mock()
    value = Mock()

    assert postgresql.postgresql_tsvector_to_json(field, value) == value
