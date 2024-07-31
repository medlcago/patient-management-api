from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.settings import settings
from utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    """
    Base class for all models
    """
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    def __repr__(self):
        package = self.__class__.__module__
        class_ = self.__class__.__name__
        attrs = ((k, getattr(self, k)) for k in self.__mapper__.columns.keys())
        sattrs = ', '.join(f'{key}={value!r}' for key, value in attrs)
        return f'{package}.{class_}({sattrs})'
