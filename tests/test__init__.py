# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy types
from celery_sqlalchemy import errors
from celery_sqlalchemy import initialize

# system imports
from unittest.mock import Mock
from unittest.mock import patch

# dependency imports
from pytest import raises

PATH = "celery_sqlalchemy"


@patch(f"{PATH}.import_module")
def test_initialize(import_module: Mock) -> None:
    celery = Mock()
    interface_module = Mock()
    import_module.return_value = interface_module

    initialize(celery)

    import_module.assert_called_with(".json", package="celery_sqlalchemy")
    interface_module.initialize.assert_called_with(celery)


@patch(f"{PATH}.import_module")
def test_initialize__raises_unsupported_interface_error(import_module: Mock) -> None:
    celery = Mock()
    import_module.side_effect = ModuleNotFoundError()

    with raises(errors.UnsupportedInterfaceError) as ex:
        initialize(celery, interface="custom")

    assert str(ex.value) == "Unsupported serialization interface 'custom'"


@patch(f"{PATH}.import_module")
def test_initialize__specify_interface(import_module: Mock) -> None:
    celery = Mock()
    interface_module = Mock()
    import_module.return_value = interface_module

    initialize(celery, interface="custom")

    import_module.assert_called_with(".custom", package="celery_sqlalchemy")


@patch(f"{PATH}.import_module")
def test_initialize__specify_interface_args(import_module: Mock) -> None:
    celery = Mock()
    interface_module = Mock()
    import_module.return_value = interface_module
    interface_args = {"arg": "value"}

    initialize(celery, interface_args=interface_args)

    interface_module.initialize.assert_called_with(celery, arg="value")
