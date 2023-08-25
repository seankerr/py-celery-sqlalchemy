# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------


class SerializationError(Exception):
    """Type cannot be serialized."""

    pass


class UnsupportedInterfaceError(Exception):
    """Serialization interface specified is unsupported."""

    pass
