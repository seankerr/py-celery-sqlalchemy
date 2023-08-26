# --------------------------------------------------------------------------------------
# Copyright (c) 2023 Sean Kerr
# --------------------------------------------------------------------------------------

# celery-sqlalchemy imports
from ..schema import TypeMap

# dependency imports
from sqlalchemy.sql import sqltypes

try:
    type_maps = {
        sqltypes.Double: TypeMap(
            from_json="double_from_json",
            params="double_params",
            to_json="double_to_json",
        ),
        sqltypes.UUID: TypeMap(
            from_json="uuid_from_json", params="uuid_params", to_json="uuid_to_json"
        ),
    }

except Exception:
    type_maps = {}
