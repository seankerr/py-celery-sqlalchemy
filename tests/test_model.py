from celery_sqlalchemy.model import _map_model

from typing import Any
from typing import cast

from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import declarative_base

import sqlalchemy as sa

Base: Any = declarative_base(metadata=sa.MetaData(schema="public"))


class Model(Base):
    __tablename__ = "model"

    array: sa.Column = sa.Column(sa.ARRAY(sa.String))
    big_integer = sa.Column(sa.BigInteger, primary_key=True)
    boolean = sa.Column(sa.Boolean)
    date = sa.Column(sa.Date)
    datetime = sa.Column(sa.DateTime(timezone=True))
    double = sa.Column(sa.Double)
    enum: sa.Column = sa.Column(sa.Enum())
    float = sa.Column(sa.Float)
    integer = sa.Column(sa.Integer)
    interval = sa.Column(sa.Interval)
    large_binary = sa.Column(sa.LargeBinary)
    json = sa.Column(sa.types.JSON)
    numeric: sa.Column = sa.Column(sa.Numeric(11, 2))
    small_integer = sa.Column(sa.SmallInteger)
    string = sa.Column(sa.String)
    text = sa.Column(sa.Text)
    time = sa.Column(sa.Time)
    unicode = sa.Column(sa.Unicode)
    unicode_text = sa.Column(sa.UnicodeText)
    uuid = sa.Column(sa.types.UUID)

    # postgreql
    postgresql_array: sa.Column = sa.Column(postgresql.ARRAY(sa.String))
    postgresql_enum: sa.Column = sa.Column(postgresql.ENUM(name="postgresql_enum"))
    postgresql_hstore = sa.Column(postgresql.HSTORE)
    postgresql_json = sa.Column(postgresql.JSON)
    postgresql_jsonb = sa.Column(postgresql.JSONB)


def test_map_model() -> None:
    mapper = cast(Mapper, sa.inspect(Model))

    _map_model(cast(DeclarativeBase, Model), mapper)

    raise Exception("unts")
