import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True)
