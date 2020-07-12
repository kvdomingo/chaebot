import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ApiSerializerMixin:
    def serialize(self, obj):
        d = {k: v for k, v in list(obj.__dict__.items())[1:]}
        return d