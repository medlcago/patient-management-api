import logging
from abc import ABC, abstractmethod
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select, func, desc, asc, Executable

from core.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.sql.base import ExecutableOption
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class Pagination(ABC):
    def __init__(
            self,
            session: "AsyncSession",
            model: type,
            limit: int | None = None,
            offset: int = 0,
            max_limit: int | None = None,
            order_by: tuple[str, bool] | None = None,
            *options: "ExecutableOption",
            **filters
    ):
        self.model = model
        self.session = session
        self.limit = limit
        self.offset = offset
        self.max_limit = max_limit or settings.pagination.max_limit
        self.order_by = order_by
        self.options = options
        self.filters = filters

    @abstractmethod
    async def get_results(self) -> Sequence:
        pass

    @abstractmethod
    async def get_count(self) -> int:
        pass

    @abstractmethod
    async def get_response(self) -> dict:
        pass

    @abstractmethod
    async def get_paginated_data(self) -> Sequence:
        pass

    @abstractmethod
    async def get_total_count(self) -> int:
        pass

    @abstractmethod
    def build_query(self) -> "Executable":
        pass

    @abstractmethod
    def build_count_query(self) -> "Executable":
        pass


class LimitOffsetPagination(Pagination):
    async def get_results(self) -> Sequence:
        try:
            results = await self.get_paginated_data()
            return results
        except Exception as ex:
            logger.error(f"Error retrieving results: {ex}")

    async def get_count(self) -> int:
        try:
            count = await self.get_total_count()
            return count
        except Exception as ex:
            logger.error(f"Error retrieving count: {ex}")

    async def get_response(self) -> dict:
        try:
            results = await self.get_results()
            return {
                "count": self.count,
                "results": results
            }
        except Exception as ex:
            logger.error(f"Error generating response: {ex}")

    async def get_paginated_data(self) -> Sequence:
        if self.limit > self.max_limit:
            self.limit = self.max_limit

        self.count = await self.get_total_count()  # noqa
        if self.count == 0 or self.offset > self.limit:
            return []

        stmt = self.build_query()
        results = (await self.session.scalars(stmt)).all()
        return results

    async def get_total_count(self) -> int:
        stmt = self.build_count_query()
        return await self.session.scalar(stmt)

    def build_query(self) -> "Executable":
        stmt = select(self.model).filter_by(**self.filters)
        if self.order_by:
            column, descending = self.order_by
            order_by = desc(getattr(self.model, column)) if descending else asc(getattr(self.model, column))
            stmt = stmt.order_by(order_by)

        stmt = stmt.limit(self.limit).offset(self.offset)
        if self.options:
            stmt = stmt.options(*self.options)
        return stmt

    def build_count_query(self) -> "Executable":
        stmt = select(func.count()).select_from(self.model).filter_by(**self.filters)
        return stmt
