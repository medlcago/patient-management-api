from typing import Optional, TYPE_CHECKING, Sequence

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from utils.pagination import LimitOffsetPagination

if TYPE_CHECKING:
    from sqlalchemy.sql.base import ExecutableOption
    from utils.pagination import Pagination


class SQLAlchemyRepository[T]:
    model: type[T] = None
    pagination_class: type["Pagination"] = LimitOffsetPagination

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count(self, **kwargs) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**kwargs)
        return await self.session.scalar(stmt)

    async def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance

    async def find_all(
            self,
            limit: int,
            offset: int,
            order_by: tuple[str, bool] | None = None,
            *options: "ExecutableOption",
            **filters
    ) -> dict[str, int | Sequence[T]]:
        return await self.pagination_class(
            session=self.session,
            model=self.model,
            limit=limit,
            offset=offset,
            order_by=order_by,
            *options,
            **filters).get_response()

    async def filter(self, many: bool = False, **kwargs) -> Optional[T] | Sequence[T]:
        stmt = select(self.model).filter_by(**kwargs)
        if many:
            return await self.session.scalars(stmt)
        return await self.session.scalar(stmt)

    async def find_by_id(self, _id: int) -> Optional[T]:
        return await self.session.get(self.model, _id)

    async def find_one(self, _id: int) -> Optional[T]:
        return await self.session.get(self.model, _id)

    async def update(self, _id: int, **kwargs) -> Optional[T]:
        stmt = update(self.model).filter_by(id=_id).values(**kwargs).returning(self.model)
        return await self.session.scalar(stmt)

    async def delete(self, instance: object) -> None:
        await self.session.delete(instance)
